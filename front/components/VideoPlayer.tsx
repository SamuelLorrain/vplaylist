import React, { useEffect } from 'react';
import { useRecoilState } from 'recoil';
import { currentPlaylistElement, playlist } from '@/contexts/recoilState';
import { Analytics } from '@/lib/analytics';

const VideoPlayer: React.FC = () => {
    const [currentPlaylistElementState, setCurrentPlaylistElementState] = useRecoilState(currentPlaylistElement);
    const [playlistState] = useRecoilState(playlist);
    const src = `http://127.0.0.1:8000/video/${currentPlaylistElementState.uuid}`;

    const analytics = new Analytics(currentPlaylistElementState.uuid);

    useEffect(() => {
        return () => {
            analytics.debug();
            analytics.send()
        }
    }, [currentPlaylistElementState.uuid]);

    return (
      <div>
        <div className="flex justify-center bg-black">
          <video height="600px"
            width="1000px"
            src={src}
            onEnded={(e) => {
              analytics.setTotalDuration(e.target.currentTime);
              const idx = currentPlaylistElementState.idx + 1;
              if (idx >= playlist.length) {
                  return;
              }
              setCurrentPlaylistElementState({
                uuid: playlistState[idx].uuid,
                idx: idx
              });
            }}
            onDurationChange={(e) => analytics.setTotalDuration(e.target.duration)}
            onTimeUpdate={(e) => analytics.updateAnalysis({type:"timeupdate", currentTime: e.target.currentTime})}
            onSeeked={(e) => analytics.updateAnalysis({type: "seek", currentTime: e.target.currentTime})}
            onPause={(e) => analytics.updateAnalysis({type: "pause", currentTime: e.target.currentTime})}
            onPlay={(e) => analytics.updateAnalysis({type: "play", currentTime: e.target.currentTime})}
            autoPlay
            controls>
          </video>
        </div>
      </div>
    );
}

export default VideoPlayer;
