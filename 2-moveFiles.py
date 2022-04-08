import os, shutil, glob

# album_name = "Trip to Tarkarli" # - 1
os.listdir()
# "Solapur Camp fire"
albums = ["CST with yash T", "Solapur get together 2021", "Sunday afternoon in Bengaluru", "Sunday afternoon in Thane", "Sunday in Bengaluru", "Sunday in Igatpuri", "Sunday in Kota", "Sunday in Mumbai", "Sunday in Shegaon", "Sunday morning at Sameer Hills", "Sunday trip in Matheran", "Team Photo session", "Thursday afternoon in Mumbai", "Thursday in Jalna", "Treat at Absolute Barbeques", "Treat at Utsav", "Trek at Matheran", "Trek to Prabalgad", "Trip at SoU", "Trip to Bandra, Worli", "Trip to Bhivpuri", "Trip to Bhogaon", "Trip to Chennai", "Trip to CST with Jatin and Tanay", "Trip to Indore and Kota", "Trip to Indore Zoo", "Trip to Jaipur and Kota", "Trip to Lavasa", "Trip to Lonavala", "Trip to Mahabaleshwar", "Trip to Mumbai and Anneswara", "Trip to Palghar during intern", "Trip to Sanjay Gandhi National Park", "Trip to Shegaon", "Trip to Solapur", "Trip to Tarkarli", "Tuesday afternoon in Mumbai", "Vihogaon falls with NSS team", "Visit to Sangi Mali in Solapur", "Waterstones waali Mumbai trip", "Weekend in Chitradurga and Davanagere", "Weekend in Jalna", "Weekend in Mumbai", "Weekend in Mumbai and Atvan", "Weekend in Palghar and Satpati"]

#  ["Trip to Tarkarli","Trip to Solapur"] # - 2
target_dir_name = "C:/Users/FM/Downloads/organised_new"


takeout_dir_name = "D:/takeout_new/Takeout/Google Photos"

for album_name in albums:
    album_dir_path = os.path.join(target_dir_name, album_name)
    if not os.path.exists(album_dir_path):
        print(album_dir_path)
        os.mkdir(album_dir_path)
    else:
        print(album_dir_path + " exists")

    try:
        takeout_dir_album_path = os.path.join(takeout_dir_name, album_name)
        file_names = os.listdir(takeout_dir_album_path)
        # Iterating over all files in takeout dir
        for file_name in file_names:
            # Moving file to album_path_dir if present in target_dir_name
            file_to_move_path = os.path.join(target_dir_name, file_name)
            if os.path.isfile(file_to_move_path):
                file_new_path = os.path.join(album_dir_path, file_name)
                print(file_to_move_path, file_new_path)
                shutil.move(file_to_move_path, file_new_path)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

    print()
