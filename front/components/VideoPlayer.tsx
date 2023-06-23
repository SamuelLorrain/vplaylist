import React, { useEffect, useRef } from 'react';
import { useRecoilState, useRecoilValue } from 'recoil';
import {
   currentPlaylistElement,
   playlist,
   globalKeydownEventIsCancelled,
   autodiscoveryMode
} from '@/contexts/recoilState';
import { Analytics } from '@/lib/analytics';
import { cancelAutoDiscover, autoDiscover } from '@/lib/autodiscover';

const VideoPlayer: React.FC = () => {
    const [currentPlaylistElementState, setCurrentPlaylistElementState] = useRecoilState(currentPlaylistElement);
    const [globalKeydownEventIsCancelledState] = useRecoilState(globalKeydownEventIsCancelled);
    const autoDiscoveryModeState = useRecoilValue(autodiscoveryMode);
    const [playlistState] = useRecoilState(playlist);
    const src = `http://127.0.0.1:8000/video/${currentPlaylistElementState.uuid}`;
    const analytics = new Analytics(currentPlaylistElementState.uuid);
    const videoRef = useRef<HTMLMediaElement>(null);

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
      <div>
        <div className="flex justify-center bg-black">
          <video height="600px"
            width="1000px"
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
            onSeeked={(e) => analytics.updateAnalysis({type: "seek", value: (e.target as HTMLMediaElement).currentTime})}
            onPause={(e) => analytics.updateAnalysis({type: "pause", value: (e.target as HTMLMediaElement).currentTime})}
            onPlay={(e) => analytics.updateAnalysis({type: "play", value: (e.target as HTMLMediaElement).currentTime})}
            autoPlay
            controls>
          </video>
        </div>
      </div>
    );
}

export default VideoPlayer;
