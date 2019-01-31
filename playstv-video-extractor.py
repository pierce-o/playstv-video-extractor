from playstvapi import *
import os

print ( "Welcome to the playtv video extractor! Please enter you username:")

# Get the users username for their account
username = input()

print ( "Now enter your password: ")

# Get the users password for the account
password = input()

# Create a new instance of the PlaysTV api class
playstv = PlaysTV( username, password )

print("Enter whether or not you want to download a single video or a profile. (S/P)")

# Ask whether or not the user wants to download a single video or all videos
is_single_video = input()

if ( is_single_video.lower() == 's' ):

    print( "Please enter the feed ID of the video you want to download: " )

    # Get the videos feed id from the user
    feed_id = input()
        
    # Get the video information    
    video = playstv.get_video_info( feed_id )['data']

    # Take the url and add the https: prefix so the request can understand the url format
    r = requests.get( "https:" + video['url'] )

    # Make sure that we have got the video successfully
    if(r.status_code == 200 and r != 'unknown'):

        # Build a folder path and file path for the video to save to using the current directory
        folder = os.getcwd() + "\\" + video['author']['urlname']
        # The video files name is that video_id
        new_file = folder + "\\" + video['video_id'] + ".mp4"

        # Make sure a folder exists    
        if( os.path.exists( folder ) == False ):
            os.makedirs( folder ) # If it doesn't create one

        # Open and create a file so that we can write to it
        file = open( new_file, "wb")

        # Notify the user that we are downloading a video, using the title to identify it
        print( "Downloading video " + video['description'] + "..." )

        # Write the videos bytes to the file
        file.write( r.content )

        # Close the file
        file.close()

elif ( is_single_video.lower() == 'p'):

    print( "Please enter the name of the profile you want to download the videos of: " )

    # Get the profiles name
    profile_name = input()

    # Get the userid of the profile, get the json object of the public videos and then finally phrase then.
    videos = playstv.phrase_video_json( playstv.get_public_videos( playstv.get_user_id( profile_name ) ) )

    # Loop through the videos array
    for video in videos:

        # Build the url 
        built_url = "https://" + video.server + "/video/" + video.videoid + "/processed/720.mp4"
        
        # Send the request
        r = requests.get( built_url )

        if(r.status_code == 200):

            # Build a folder path and file path for the video to save to using the current directory    
            folder = os.getcwd() + "\\" + profile_name
            new_file = folder + "\\" + video.videoid + ".mp4"

            # Make sure a folder exists    
            if( os.path.exists( folder ) == False ):
                os.makedirs( folder ) # If it doesn't create one

            # Open and create a file so that we can write to it
            file = open( new_file, "wb")

            # Notify the user that we are downloading a video, using the title to identify it
            print( "Downloading video " + video.description + "..." )

            # Write the videos bytes to the file
            file.write( r.content )

            # Close the file
            file.close()

        # Once the loop has ended then notify the user that all of the videos have downloaded
        print ( "All files have successfully downloaded!")

else: # Unknown command, exit
    exit()