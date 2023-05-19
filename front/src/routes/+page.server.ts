import type { PageLoad } from './$types';

export const load = (async ({ url }) => {
    let fetchUrl : URL = new URL('http://127.0.0.1:8000/playlist/create')
    for(let [key,value] of url.searchParams) {
        if (key === 'best' && value === 'true') {
            fetchUrl.searchParams.set('search_type', 'best');
        }
        if (key === 'last' && value === 'true') {
            fetchUrl.searchParams.set('sorting', 'last_by_id');
        }
        if (key === 'search' && value !== '') {
            fetchUrl.searchParams.set('search_type', 'basic');
            fetchUrl.searchParams.set('search_term', value);
        }
        if (key === 'no_webm' && value === 'true') {
            fetchUrl.searchParams.set('webm', 'no_webm');
        }
    }
    const response = await fetch(fetchUrl)
    const content = await response.json()
    return {
       playlist: content.playlist,
    }
}) satisfies PageLoad;
