def gstreamer_command_create(input_data, camera_data, output_data):
    """
    根据传入和传出生成GStreamer语句
    """
    gstreamer_command = ""
    for input_ in input_data:
        if input_["type"] == "Image":
            """
            appsrc name=source is-live=true format=time caps="image/png, framerate=30/1" ! \
            pngdec ! \
            videoconvert ! \
            tee name=t ! \
            queue max-size-buffers=10 ! appsink name=imgsink drop=false max-buffers=10 \
            t. ! queue ! \
            x264enc tune=zerolatency speed-preset=ultrafast bitrate=3000 key-int-max=60 bframes=0 ! \
            queue max-size-buffers=50 ! mux. \
            """
        if input_["type"] == "Video":
            """
            appsrc name=source is-live=true format=time caps="image/png, framerate=30/1" ! \
            pngdec ! \
            videoconvert ! \
            tee name=t ! \
            queue max-size-buffers=10 ! appsink name=imgsink drop=false max-buffers=10 \
            t. ! queue ! \
            x264enc tune=zerolatency speed-preset=ultrafast bitrate=3000 key-int-max=60 bframes=0 ! \
            queue max-size-buffers=50 ! mux. \
            """
        if input_["type"] == "Stream":
            f"""
            rtspsrc location={camera_data['rtsp_url']} latency=0 ! \
            {'rtph264depay' if camera_data["encode"] == 'H264' else 'rtph265depay'} ! \
            {'avdec_h264' if camera_data["encode"] == 'H264' else 'avdec_h265'} ! \
            videoconvert ! \
            tee name=t ! \
            queue max-size-buffers=10 ! appsink name=imgsink drop=false max-buffers=10 \
            t. ! queue ! \
            x264enc tune=zerolatency speed-preset=ultrafast bitrate=3000 key-int-max=60 bframes=0 ! \
            queue max-size-buffers=50 ! mux. \
            """
        if input_["type"] == "SoundCard":
            """
            alsasrc device="hw:1,0" ! audioconvert ! audioresample ! tee name=t1 \
            t1. ! queue ! appsink name=audiosink drop=false max-buffers=10 \
            """

    gstreamer_command = gstreamer_command + """
        appsrc name=audio_appsrc is-live=true format=time do-timestamp=true ! \
        decodebin ! audioconvert ! avenc_aac ! queue max-size-buffers=50 ! mux. \
        mpegtsmux name=mux ! \
    """
    if output_data == "Audio":
        gstreamer_command = gstreamer_command + """
        decodebin ! audioconvert ! audioresample ! alsasink device="hw:1,0"
        """
    else:
        gstreamer_command = gstreamer_command + """
        output = f"rtspclientsink location={gstreamer_config['gs_output_data']}"
        """