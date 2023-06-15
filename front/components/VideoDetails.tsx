import { useVideoDetails } from '@/hooks/videoDetails';
import React from 'react';

const VideoDetails: React.FC<{uuid: string|null}> = ({uuid}: {uuid:string|null}) => {
    const { data, error } = useVideoDetails(uuid);

    if (error) {
        return "error";
    }
    if (data) {
        return (<div className="p-2 border rounded-b-md">
            <h2>{data.path ?? data.name ?? data.uuid}</h2>
        </div>);
    }
    return "loading..."

}

export default VideoDetails;
