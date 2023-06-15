import { PlaylistContext } from '@/contexts/PlaylistContext';
import { fetcher } from '@/lib/fetchers';
import { useContext } from 'react';

import useSWR from 'swr';

export function useGetNewPlaylistUrl() {
    const { fetchingOptions, search } = useContext(PlaylistContext);

    let fetchUrl : URL = new URL('http://127.0.0.1:8000/playlist/create')
    if (fetchingOptions.best) {
        fetchUrl.searchParams.set('search_type', 'best');
    }
    if (fetchingOptions.last) {
        fetchUrl.searchParams.set('sorting', 'last_by_id');
    }
    if (search) {
        fetchUrl.searchParams.set('search_type', 'basic');
        fetchUrl.searchParams.set('search_term', search);
    }
    if (fetchingOptions.noWebm) {
        fetchUrl.searchParams.set('webm', 'no_webm');
    }
    fetchUrl.searchParams.set('quality', fetchingOptions.quality);
    return fetchUrl;
};

export function useNewPlaylist() {
    const fetchUrl = useGetNewPlaylistUrl();
    const { data, error }= useSWR(
        fetchUrl.toString(),
        fetcher,
        {
            revalidateOnFocus: false,
            revalidateOnReconnect: false,
        }
    );
    return {
        data,
        error,
        fetchUrl,
    }
}


export function useVideoDetails(uuid: string|null) {
    console.log("uuid, ", uuid);
    const { data, error }= useSWR(
        () => (uuid != null) ? `http://localhost:8000/video/${uuid}/details` : null,
        fetcher
    );
    return {
        data,
        error
    };
}
