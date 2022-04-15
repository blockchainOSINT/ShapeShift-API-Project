
import requests, json, time, os
from datetime import datetime
from sys import argv
from pymongo import MongoClient

script, num_to_process = argv


def load_txData(data_file):
    """Load transaction data scraped from BTC blockchain by getTxData_BTC_RPC.py"""

    with open(data_file) as f:
        txData = []
        for line in f:
            txData.append(json.loads(line.strip()))

    print(f"Addresses to check: {len(txData)}", '\n')

    return txData


def checkSS(valid_txData, save_file):
    """Query the ShapeShift API for possible target transactions"""

    total_queries = 0
    speed_log = 0
    start_time = time.time()
    txStats = []
    errors = []

    with open(save_file, 'a') as file:
        for data in valid_txData:
            address, txid, block_height, timestampUNIX  = data
            timestamp_utc = datetime.utcfromtimestamp(timestampUNIX).strftime('%Y-%m-%d %H:%M:%S')
            url = f"https://shapeshift.io/txstat/{address}"

            try:

                response = requests.get(url=url)
                total_queries += 1
                speed_log += 1

                if response.status_code == 200:
                    response_json = response.json()
                    if response_json["status"] != "error":
                        response_json["incomingTXID"] = txid; response_json["timestampUTC"] = timestamp_utc;  response_json["timestampUNIX"] = timestampUNIX;
                        response_json["fromBlock"] = block_height
                        print(response_json, "\n")
                        txStats.append(json.dumps(response_json))
                        file.write(json.dumps(response_json)+'\n')
                else:
                    print("\nError:", url, "\n")
                    errors.append(data)
            except:
                errors.append(data)
                
                
            # output performance stats    
            if speed_log == 100:
                percent_complete = round(total_queries / len(valid_txData) * 100, 1)
                speed = round(total_queries / (time.time() - start_time) * 3600, 1)
                queries_remaining = (len(valid_txData) - total_queries)
                est_time_remaining = round(queries_remaining / speed * 60, 1)
                print("\t\t\t\tSpeed:", speed, "queries / hr", "\n\t\t\t\tEst. Time Remaining:", est_time_remaining, "minutes", f"\n\t\t\t\t{percent_complete}% complete\n")
                speed_log = 0

    return txStats, total_queries, errors, save_file


def retryErrors(errors, txStats, save_file):
    """Sometime the API doesn't respond. This function will retry failed responses to ensure best coverage."""
    
    unresolved_errors = []
    save_blocks = save_file.split("_")[1]

    with open(save_file, 'a') as file:
        for txData in errors:
            address, txid, block_height, timestampUNIX  = txData
            timestamp_utc = datetime.utcfromtimestamp(timestampUNIX).strftime('%Y-%m-%d %H:%M:%S')
            url = f"https://shapeshift.io/txstat/{address}"

            try:
                response = requests.get(url=url)
                if response.status_code == 200:
                    response_json = response.json()
                    if response_json["status"] != "error":
                        response_json["incomingTXID"] = txid; response_json["timestampUTC"] = timestamp_utc;  response_json["timestampUNIX"] = timestampUNIX;
                        response_json["fromBlock"] = block_height
                        print(response_json, "\n")
                        txStats.append(json.dumps(response_json))
                        file.write(json.dumps(response_json)+'\n')
                else:
                    print("\nError:", url, "\n")
                    unresolved_errors.append(txData)
            except:
                unresolved_errors.append(txData)

    if unresolved_errors:
        with open(f"UNRESOLVED_ERRORS_{save_blocks}.txt", "a") as f:
            for error in unresolved_errors:
                f.write(json.dumps(error)+'\n')

    return unresolved_errors, txStats

def uploadResults(txStats, save_file):
    """Automatically upload the results to MongoDB"""
    
    # convert txStats from strings back to to dicts to enable MongoDB insertion
    txStats = [json.loads(txStat) for txStat in txStats]
    
    # login details redacted for privacy
    try:
        connection_string = 'mongodb+srv://{USERNAME}:{PASSWORD}@sandbox.txcmx.mongodb.net/ShapeShift?retryWrites=true&w=majority'    
        client = MongoClient(connection_string)
        db = client.ShapeShift
        collection = db.BTC
        collection.insert_many(txStats)
        print("\nTotal Documents:", collection.count_documents({}))
        upload_status = "Successful"
    except:
        print("Connection Unsuccessful")
        with open("Unsuccess Uploads.txt", 'a+') as f:
            f.write(save_file+'\n')
        upload_status = "UNSUCCESSFUL"
        
    return upload_status

def main(data_file, save_file):

    start_time = time.time()

    print("\nProcessing File:", data_file, "\n\nStart Time:", time.ctime(start_time))

    txData = load_txData(data_file)
    txStats, total_queries, errors, save_file = checkSS(txData, save_file)
    unresolved_errors, txStats = retryErrors(errors, txStats, save_file)
    upload_status = uploadResults(txStats, save_file)

    finish_time = time.time()
    time_elapsed = round((finish_time - start_time) / 60, 2)
    avg_speed = round(total_queries / time_elapsed * 60, 1)
    finished_alert ="\a"
    
    # output performace stats
    print("\nFinish Time:", time.ctime(finish_time), "\n\nTotal Queries:", total_queries, "\nResults Found:", len(txStats), "\nErrors:", len(errors),
          "\nResolved Errors:", len(errors) - len(unresolved_errors), "\nUnresolved Errors:", len(unresolved_errors),
          "\nTime Elapsed (min):", time_elapsed, "\nAverage Speed:", avg_speed, "queries per hour\n", finished_alert, "Upload Status:", upload_status, '\n')

    print('\nSaving File:', save_file, '\nDeleting File:', data_file, '\n')
    
    # auto-remove txData from server (backups saved locally)
    os.remove(data_file)


def autoRun():
    """Run the script a specified number of times as specified in command line argv (one txData files averages 2 hrs to complete)"""

    file_list = [x for x in os.listdir('.') if 'BTC_txData' in x]
    file_list.sort()
    file_list = file_list[0:int(num_to_process)]
    for data_file in file_list:
        save_blocks = data_file.split("_")[2]
        save_file = f"RESULTS_{save_blocks}" # automate save file to eliminate naming mistakes

        if __name__ == "__main__":
            main(data_file, save_file)

autoRun()
