import React from 'react';

const VideoPlayer: React.FC<{uuid: string|null}> = ({uuid}) => {
    let src = "";
    if (uuid) {
        src = `http://127.0.0.1:8000/video/${uuid}`;
    }

    return <div>
        <div className="flex justify-center bg-black">
            <video height="600px" width="1000px" src={src} autoPlay controls>
            </video>
        </div>
    </div>;
}

export default VideoPlayer;
