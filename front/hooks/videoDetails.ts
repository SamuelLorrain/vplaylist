import { fetcher } from '@/lib/fetchers';
import { searchOptions, authenticationToken } from '@/contexts/recoilState';
import { useRecoilState, useRecoilValue } from 'recoil';

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
    const token = useRecoilValue(authenticationToken);
    const { data, error }= useSWR(
        token && {url: fetchUrl.toString(), token},
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
    const token = useRecoilValue(authenticationToken);
    const { data, error }= useSWR(
        () => (uuid && token) ? {url:`${process.env.NEXT_PUBLIC_BACK_HOST}/video/${uuid}/details`, token} : null,
        fetcher,
        {
            revalidateOnFocus: false,
            revalidateOnReconnect: false,
        }
    );
    return {
        data,
        error
    };
}
