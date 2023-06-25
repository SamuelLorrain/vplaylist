import React, { useEffect, useRef, useState } from 'react';
import { useRecoilState, useRecoilValue } from 'recoil';
import {
   currentPlaylistElement,
   playlist,
   globalKeydownEventIsCancelled,
   autodiscoveryMode
} from '@/contexts/recoilState';
import { Analytics } from '@/lib/analytics';
import { cancelAutoDiscover, autoDiscover } from '@/lib/autodiscover';
import { Play, Pause, Maximize, Shrink } from 'lucide-react';
import { Progress } from '@/components/ui/progress';
import { cn } from '@/lib/utils';

const HIDE_CONTROL_TIMEOUT_TIME= 3000;

function getIsVideoPlaying(videoEl: HTMLMediaElement|null) {
    if (videoEl == null) {
        return false;
    }
    return !!(videoEl.currentTime > 0 && !videoEl.paused && !videoEl.ended && videoEl.readyState > 2);
}

function getPlayingPercentage(videoEl: HTMLMediaElement|null) {
    if (videoEl == null || videoEl.duration === 0) {
        return 0;
    }
    return (videoEl.currentTime / videoEl.duration) * 100;
}

function seekWithClick(videoEl: HTMLMediaElement|null, progressBar: any, event: any) {
    if (event.target.clientWidth === 0 || videoEl == null || progressBar == null) {
        return 0;
    }
    const ratio = (event.pageX - (progressBar.offsetLeft + progressBar.offsetParent.offsetParent.offsetLeft)) / progressBar.clientWidth;
    if (ratio == 0) {
        return 0;
    }
    return videoEl.duration * ratio;
}

function togglePlay(videoEl: HTMLMediaElement|null, setter) {
    if (videoEl == null) {
        return;
    }
    if (getIsVideoPlaying(videoEl)) {
        videoEl.pause();
        setter(false);
    } else {
        videoEl.play()
        .then(() => setter(true));
    }
}

const VideoPlayer: React.FC = () => {
    const [currentPlaylistElementState, setCurrentPlaylistElementState] = useRecoilState(currentPlaylistElement);
    const [globalKeydownEventIsCancelledState] = useRecoilState(globalKeydownEventIsCancelled);
    const autoDiscoveryModeState = useRecoilValue(autodiscoveryMode);
    const [playlistState] = useRecoilState(playlist);
    const src = `http://127.0.0.1:8000/video/${currentPlaylistElementState.uuid}`;
    const analytics = new Analytics(currentPlaylistElementState.uuid);
    const [isVideoPlaying, setIsVideoPlaying] = useState(false);
    const [playingPercentage, setPlayingPercentage] = useState(0);
    const [isFullScreen, setIsFullScreen] = useState(false);
    const [isDisplayingControl, setIsDisplayingControl] = useState(false);
    const [currentDisplayingControlTimeout, setCurrentDisplayingControlTimeout] = useState<any>(null);

    const videoRef = useRef<HTMLMediaElement>(null);
    const videoContainerRef = useRef<HTMLDivElement>(null);
    const progressBarRef = useRef<HTMLDivElement>(null);


    useEffect(() => {
        const fullScreenChangeHandler = () => {
            if (document.fullscreenElement) {
                setIsFullScreen(true);
            } else {
                setIsFullScreen(false);
            }
        };
        document.addEventListener('fullscreenchange', fullScreenChangeHandler);
        return () => {
            removeEventListener('fullscreenchange', fullScreenChangeHandler)
        }
    }, []);

    useEffect(() => {
        const videoEl = videoRef.current;
        if (videoEl == null) {
            return;
        }
        setTimeout(() => setIsVideoPlaying(getIsVideoPlaying(videoEl)), 500);
    }, [videoRef.current, currentPlaylistElementState.uuid]);

    useEffect(() => {
        if (videoRef.current == null) {
            return;
        }
        if(!autoDiscoveryModeState){
            cancelAutoDiscover(videoRef.current);
            return;
        }
        autoDiscover(videoRef.current);
        return () => {
            if (videoRef.current == null) {
                return;
            }
            cancelAutoDiscover(videoRef.current);
        }
    }, [autoDiscoveryModeState, videoRef.current]);

    useEffect(() => {
        let clickEvent = (e: KeyboardEvent) => {
            if (autoDiscoveryModeState) {
                return;
            }
            if (globalKeydownEventIsCancelledState) {
                return;
            }
            if (videoRef.current == null) {
                return;
            }
            const video: HTMLMediaElement = videoRef.current;
            if(e.code === "Space") {
                video.paused ? video.play() : video.pause();
            } else if (e.key === ">") {
                const idx = (currentPlaylistElementState.idx + 1);
                if (idx >= playlistState.length) {
                    return;
                }
                setCurrentPlaylistElementState({
                  uuid: playlistState[idx].uuid,
                  idx: idx
                });
            } else if (e.key === "<") {
                if (currentPlaylistElementState.idx - 1 < 0) {
                    return;
                }
                setCurrentPlaylistElementState({
                  uuid: playlistState[currentPlaylistElementState.idx - 1].uuid,
                  idx: currentPlaylistElementState.idx - 1
                });
            }
        };
        window.addEventListener("keydown", clickEvent);
        return () => {
            removeEventListener("keydown", clickEvent)
        };
    }, [JSON.stringify(currentPlaylistElementState), playlistState.length, globalKeydownEventIsCancelledState]);

    useEffect(() => {
        return () => {
            if(!autoDiscoveryModeState){
                analytics.send()
            }
        }
    }, [currentPlaylistElementState.uuid, autoDiscoveryModeState]);

    return (
    <div className="relative"
         ref={videoContainerRef}
         onMouseEnter={() => {
           if(currentDisplayingControlTimeout) {
            clearTimeout(currentDisplayingControlTimeout);
           }
           setIsDisplayingControl(true)
           const timeoutId = setTimeout(() => setIsDisplayingControl(false), HIDE_CONTROL_TIMEOUT_TIME);
           setCurrentDisplayingControlTimeout(timeoutId);
         }}
         onMouseMove={() => {
           if(currentDisplayingControlTimeout) {
            clearTimeout(currentDisplayingControlTimeout);
           }
           setIsDisplayingControl(true)
           const timeoutId = setTimeout(() => setIsDisplayingControl(false), HIDE_CONTROL_TIMEOUT_TIME);
           setCurrentDisplayingControlTimeout(timeoutId);
         }}
         onMouseLeave={() => {
           if(currentDisplayingControlTimeout) {
            clearTimeout(currentDisplayingControlTimeout);
           }
           const timeoutId = setTimeout(() => setIsDisplayingControl(false), HIDE_CONTROL_TIMEOUT_TIME);
           setCurrentDisplayingControlTimeout(timeoutId);
         }}
    >
      <div className="flex justify-center items-center bg-black">
        <video
          height={isFullScreen ? "auto" : "600px"}
          width={isFullScreen ? "100%" : "1000px"}
          ref={videoRef}
          id="video-player"
          src={src}
          onEnded={(_) => {
            analytics.updateAnalysis({type: "ended", value: -1})
            const idx = currentPlaylistElementState.idx + 1;
            if (idx >= playlistState.length) {
                return;
            }
            setCurrentPlaylistElementState({
              uuid: playlistState[idx].uuid,
              idx: idx
            });
          }}
          onClick={() => {!globalKeydownEventIsCancelledState && togglePlay(videoRef.current, setIsVideoPlaying)}}
          onSeeked={(e) => analytics.updateAnalysis({type: "seek", value: (e.target as HTMLMediaElement).currentTime})}
          onTimeUpdate={(e) => {
            setPlayingPercentage(getPlayingPercentage(e.target as HTMLMediaElement))
          }}
          onPause={(e) => {
              if (videoRef.current == null) return;
              analytics.updateAnalysis({type: "pause", value: (e.target as HTMLMediaElement).currentTime})
            }
          }
          onPlay={(e) => {
              if (videoRef.current == null) return;
              analytics.updateAnalysis({type: "play", value: (e.target as HTMLMediaElement).currentTime})
            }
          }
          >
        </video>
      </div>
      <div className={cn("video-controls-container", isDisplayingControl ? '' : 'invisible')}
           onClick={() => togglePlay(videoRef.current, setIsVideoPlaying)}
      >
        <div className="flex justify-end h-full">
          <div className="video-controls-playlist-container">
          </div>
        </div>
        <div className="video-controls flex gap-2 p-2 items-center"
             onMouseEnter={(e) => {
               e.stopPropagation();
               if(currentDisplayingControlTimeout) {
                clearTimeout(currentDisplayingControlTimeout);
               }
               setIsDisplayingControl(true)
             }}
             onMouseMove={(e) => {
                e.stopPropagation()
                if(currentDisplayingControlTimeout) {
                 clearTimeout(currentDisplayingControlTimeout);
                }
                setIsDisplayingControl(true)
             }}
        >
          {
            isVideoPlaying ?
            <Pause className="cursor-pointer" color="white" onClick={(e) => {e.stopPropagation(); togglePlay(videoRef.current, setIsVideoPlaying)}}/>
            :
            <Play className="cursor-pointer" color="white" onClick={(e) => {e.stopPropagation(); togglePlay(videoRef.current, setIsVideoPlaying)}}/>
          }
          <Progress
            ref={progressBarRef}
            className="h-2 cursor-pointer"
            value={playingPercentage} max={100} onClick={(e) => {e.stopPropagation(); videoRef?.current?.fastSeek(seekWithClick(videoRef.current, progressBarRef.current, e))}}
          />
          {
            !isFullScreen ?
            <Maximize className="cursor-pointer" color="white" onClick={(e) => {
                e.stopPropagation();
                videoContainerRef?.current?.requestFullscreen().then(() => setIsFullScreen(true))
            }}/>
            :
            <Shrink className="cursor-pointer" color="white" onClick={(e) => {
                e.stopPropagation();
                document.exitFullscreen().then(() => setIsFullScreen(false));
            }}/>
          }
        </div>
      </div>
    </div>
    );
}

export default VideoPlayer;

