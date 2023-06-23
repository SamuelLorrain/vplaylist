const autoDiscoverMap: Map<string, ReturnType<typeof setInterval>> = new Map();

export const autoDiscover = (media: HTMLMediaElement) => {
    if (media.played) {
        media.pause();
    }
    const interval = setInterval(() => {
        if (media.paused) {
            media.play()
            .then(() => {
                const duration = media.duration;
                const seek = Math.floor(duration/10);
                media.fastSeek(media.currentTime + seek);
            })
        } else {
            const duration = media.duration;
            const seek = Math.floor(duration/10);
            media.fastSeek(media.currentTime + seek);
        }

    }, 2000);
    autoDiscoverMap.set(media.id, interval);
}

export const cancelAutoDiscover = (media: HTMLMediaElement) => {
    media.pause();
    clearInterval(autoDiscoverMap.get(media.id));
    autoDiscoverMap.delete(media.id);
}
