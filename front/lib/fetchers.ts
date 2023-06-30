export const fetcher = async ({url, token}: {url: string, token: string}) => {
    return fetch(url, {
        headers: {
            'Authorization': 'Bearer ' + token
        }
    }).then(res => res.json())
}

