import React, { useContext, useEffect } from 'react';
import { Separator } from '@/components/ui/separator';
import { useNewPlaylist } from '@/hooks/videoDetails';
import { PlaylistContext } from '@/contexts/PlaylistContext';

export default function Playlist() {
    const { data, error } = useNewPlaylist()
    const { setCurrentUUID, setData, currentUUID } = useContext(PlaylistContext);

    useEffect(() => {
        setData(data);
        if (data?.playlist.length > 0) {
            setCurrentUUID(data?.playlist[0].uuid);
        }
    }, [JSON.stringify(data), setData])

    if (error) return "error";
    if (data) {
        return (
            <div className="playlist border-t border-x rounded-md overflow-y-scroll overflow-x-hidden">
            {
                data.playlist.map((point: {uuid: string, path: string}) =>
                <div key={point.uuid}>
                    <div className={
                       (point.uuid === currentUUID) ?
                       "bg-secondary/100 p-2" :
                       "hover:bg-secondary/80 cursor-pointer p-2"
                    }>
                        <div onClick={() => setCurrentUUID(point.uuid)}>
                            {point.path}
                        </div>
                    </div>
                    <Separator/>
                </div>
                )
            }
            </div>
        );
    }
    return <div>is loading...</div>;
}
