"use client";

import { useState, useEffect } from 'react';
import Toolbar from '@/components/Toolbar';
import VideoPlayer from '@/components/VideoPlayer';
import Playlist from '@/components/Playlist';
import VideoDetails from '@/components/VideoDetails';
import { PlaylistContext, PlaylistDataType } from '@/contexts/PlaylistContext';

export default function Home() {
    const [currentUUID, setCurrentUUID] = useState<string|null>(null);
    const [data, setData] = useState<PlaylistDataType|null>(null)
    const [quality, setQuality] = useState('all');
    const [noWebm, setNoWebm] = useState(false);
    const [last, setLast] = useState(false);
    const [best, setBest] = useState(false);
    const [search, setSearch] = useState('');

    // setUUID onload
    useEffect(() => {
        if (!data || currentUUID) {
            return;
        }
        if (data?.playlist.length > 0) {
            setCurrentUUID(data?.playlist[0].uuid);
        }
    }, [data, currentUUID, setCurrentUUID])

    return (
        <PlaylistContext.Provider value={{
            currentUUID,
            data,
            setData,
            setCurrentUUID,
            fetchingOptions: {
                noWebm,
                quality,
                last,
                best
            },
            setFetchingOptions: ({noWebm, quality, last, best}: {noWebm: boolean, quality: string, last: boolean, best: boolean}) => {
                setNoWebm(noWebm);
                setQuality(quality);
                setLast(last);
                setBest(best);
            },
            search,
            setSearch
        }}>
            <div className="mb-5">
                <Toolbar/>
                <div className="flex px-20 gap-5">
                    <div className="w-2/3">
                        <VideoPlayer uuid={currentUUID}/>
                        <VideoDetails uuid={currentUUID}/>
                    </div>
                    <div className="w-1/3">
                        <Playlist/>
                    </div>
                </div>
            </div>
        </PlaylistContext.Provider>
    );
}
