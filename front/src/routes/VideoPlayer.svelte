<script>
    import { onMount } from 'svelte';
    export let src;
    export let currentVideo;
    export let endVideoCallback;
    export let previousVideoCallback;
    export let nextVideoCallback;
    export let errorVideoCallback;

    let videoElement;

    onMount(() => {
        videoElement.addEventListener("ended", endVideoCallback);
        videoElement.addEventListener("error", errorVideoCallback);

        window.addEventListener('keypress', (e) => {
            if (e.key === 'p') {
                if (videoElement.paused) {
                    videoElement.play();
                } else {
                    videoElement.pause();
                }
            } else if (e.key === '>') {
                nextVideoCallback();
            } else if (e.key === '<') {
                previousVideoCallback();
            } else if (e.key === 'f') {
                videoElement.requestFullScreen();
            }
        });

        return () => {
            videoElement.removeEventListener("ended", endVideoCallback);
            videoElement.removeEventListener("error", errorVideoCallback);
        }
    })
</script>

<div>
    <div class="video-container">
        <video bind:this={videoElement} controls src={src} height="600" autoplay/>
    </div>
    <div class="video-title">{currentVideo.path}</div>
</div>

<style>
.video-container {
    display:flex;
    justify-content:center;
    border: 1px solid black;
    background-color: black;
}

.video-title {
    text-align: center;
    margin-bottom: 1rem;
}
</style>
