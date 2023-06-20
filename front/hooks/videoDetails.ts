import { fetcher } from '@/lib/fetchers';
import { searchOptions } from '@/contexts/recoilState';
import { useRecoilState } from 'recoil';

import useSWR from 'swr';

export function useGetNewPlaylistUrl() {
  const [fetchContext, _] = useRecoilState(searchOptions);

    let fetchUrl : URL = new URL('http://127.0.0.1:8000/playlist/create')
    if (fetchContext.fetchingOptions.best) {
        fetchUrl.searchParams.set('search_type', 'best');
    }
    if (fetchContext.fetchingOptions.last) {
        fetchUrl.searchParams.set('sorting', 'last_by_id');
    }
    if (fetchContext.search.length > 0) {
        fetchUrl.searchParams.set('search_type', 'basic');
        fetchUrl.searchParams.set('search_term', fetchContext.search);
    }
    if (fetchContext.fetchingOptions.noWebm) {
        fetchUrl.searchParams.set('webm', 'no_webm');
    }
    fetchUrl.searchParams.set('quality', fetchContext.fetchingOptions.quality);
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
    const { data, error }= useSWR(
        () => (uuid != null) ? `http://localhost:8000/video/${uuid}/details` : null,
        fetcher
    );
    return {
        data,
        error
    };
}
