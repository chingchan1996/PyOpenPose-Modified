"""
Example script using PyOpenPose.
"""
import PyOpenPose as OP
import time
import cv2

import numpy as np
import os
import sys
import logging as lg

OPENPOSE_ROOT = os.environ["OPENPOSE_ROOT"]


def showHeatmaps(hm):
    for idx, h in enumerate(hm):
        cv2.imshow("HeatMap "+str(idx), h)


def showPAFs(PAFs, startIdx=0, endIdx=16):
    allpafs = []
    for idx in range(startIdx, endIdx):
        X = PAFs[idx*2]
        Y = PAFs[idx*2+1]
        tmp = np.dstack((X, Y, np.zeros_like(X)))
        allpafs.append(tmp)

    pafs = np.mean(allpafs, axis=0)
    cv2.imshow("PAF", pafs)

def writeKeyPoints( pose, frameCounter, outputFile):

    frameNo = "Frame No." + str(frameCounter) + '\n'
    outputFile.write( frameNo )
    lg.info( frameNo )

    totalpeople = 'Total people:' + str(len(pose)) + '\n'
    outputFile.write( totalpeople ) 
    lg.info( totalpeople )

    for i in range( 0, len(pose) ):

        pplNo = 'No.' + str(i+1) + '\n'
        outputFile.write( pplNo ) 
        lg.info( pplNo )

        for p in pose[i]:

            outputFile.write(str(p))
            lg.info( str(p) )

            outputFile.write('\n')

        outputFile.write('\n\n') 
        lg.info('\n\n')



def run( _filename, _show, _standard):

    cap = cv2.VideoCapture(0)
    fileName = _filename
    is_open = cap.open(fileName)

    if _show:
        lg.getLogger().setLevel( lg.INFO)


    lg.info( '  Media read:' + str(is_open) )


    outputFileName = ('output_' + fileName + '.txt')
    outputFile = open( str(outputFileName), 'w' )
    

    lg.info( '  ' + str(outputFile) ) 

    download_heatmaps = False
    op = OP.OpenPose((320, 240), (240, 240), (640, 480), "COCO", OPENPOSE_ROOT + os.sep + "models" + os.sep, 0, download_heatmaps)
    
    actual_fps = 0
    paused = False
    delay = {True: 0, False: 1}

    lg.info("  Entering main Loop.")
    ret, frame = cap.read()
    frameCounter = 1
    while True:
        start_time = time.time()
        try:
            ret, frame = cap.read()
            rgb = frame

        except Exception as e:
            print("Failed to grab", e)
            break

        t = time.time()
        try:
            op.detectPose(rgb)
        except Exception as e:
            break

        t = time.time() - t
        op_fps = 1.0 / t
        res = op.render(rgb)
        cv2.putText(res, 'UI FPS = %f, OP FPS = %f' % (actual_fps, op_fps), (20, 20), 0, 0.5, (0, 0, 255))
        persons = op.getKeypoints(op.KeypointType.POSE)
        
        if persons[0] is not None:
            
            pose = persons[0] 
            score = persons[1]
            result_pose = []
            result_score = []
            i = 0 
            for sc in score:
                if sc > _standard:
                    result_pose.append( pose[i] ) 
                    result_score.append( sc )
                i = i + 1 
            # end of for-loop

            if len(result_score) > 0:
                writeKeyPoints( result_pose, frameCounter, outputFile )

        if _show:
            cv2.imshow("OpenPose result", res)
            key = cv2.waitKey(delay[paused])
            if key & 255 == ord('p'):
                paused = not paused

            if key & 255 == ord('q'):
                break

        actual_fps = 1.0 / (time.time() - start_time)
        frameCounter = frameCounter + 1



    outputFile.close()

    lg.info( outputFile ) 

if __name__ == '__main__':

    if sys.argv[1] == None:
        filename = input('Enter the file name with extension:\n')
    else:
        filename = str(sys.argv[1])

    if sys.argv[2] == None:
        show = True
    else:
        if sys.argv[2] == 'False':
            show = False
        else:
            show = True 

    print(show)
    input()

    if sys.argv[3] == None:
        standard = 0.5
    else:
        standard = float(sys.argv[3])
        
    run( filename, show, standard)
