import React, { useEffect } from 'react';
import { Separator } from '@/components/ui/separator';
import { useNewPlaylist } from '@/hooks/videoDetails';
import { useRecoilState } from 'recoil';
import { playlist, currentPlaylistElement } from '@/contexts/recoilState';

export default function Playlist() {
    const { data, error } = useNewPlaylist()
    const [playlistState, setPlaylistState] = useRecoilState(playlist);
    const [currentPlaylistElementState, setCurrentPlaylistElementState] = useRecoilState(currentPlaylistElement);

    useEffect(() => {
        if (data?.playlist?.length > 0) {
            setPlaylistState(data.playlist);
            setCurrentPlaylistElementState({idx:0, uuid: data.playlist[0].uuid});
        } else {
            setPlaylistState([]);
            setCurrentPlaylistElementState({idx:-1, uuid: ''});
        }
    }, [JSON.stringify(data)]);

    function updateCurrentMedia(uuid: string, idx: number) {
        setCurrentPlaylistElementState({uuid: uuid, idx: idx});
    }

    if (error) {
        return "error";
    }
    if (data) {
        return (
            <div className="playlist border-t border-x rounded-md overflow-y-scroll overflow-x-hidden">
            {
                playlistState.map((point: {uuid: string, path: string}, idx) =>
                <div key={point.uuid} onClick={() => updateCurrentMedia(point.uuid, idx)}>
                    <div className={
                       (point.uuid === currentPlaylistElementState.uuid) ?
                       "bg-secondary/100 p-2 flex h-32" :
                       "hover:bg-secondary/80 cursor-pointer p-2 flex h-32"
                    }>
                        <div className="bg-black h-15 w-1/2 shrink-0 flex justify-center items-center overflow-hidden border-2 border-black">
                            <img src={`${process.env.NEXT_PUBLIC_BACK_HOST}/static/thumbnails/${point.uuid}.jpg`} className="overflow-hidden block"/>
                        </div>
                        <div className="pl-1 w-1/2 shrink-0 overflow-hidden">
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

