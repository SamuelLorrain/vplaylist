import React from 'react';
import { useRecoilState } from 'recoil';
import { currentPlaylistElement } from '@/contexts/recoilState';

const VideoPlayer: React.FC = () => {
    const [currentPlaylistElementState] = useRecoilState(currentPlaylistElement);
    const src = `http://127.0.0.1:8000/video/${currentPlaylistElementState.uuid}`;

    return (
    <div>
      <div className="flex justify-center bg-black">
        <video height="600px" width="1000px" src={src} autoPlay controls>
        </video>
      </div>
    </div>);
}

export default VideoPlayer;
