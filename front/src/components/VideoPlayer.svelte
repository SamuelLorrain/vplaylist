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
                if (!document.fullScreenElement) {
                    videoElement.requestFullscreen();
                } else {
                    videoElement.exitFullscreen();
                }
            }
        });

        return () => {
            videoElement.removeEventListener("ended", endVideoCallback);
            videoElement.removeEventListener("error", errorVideoCallback);
        }
    })
</script>

<div>
    <div class="bg-black flex justify-center">
        <video bind:this={videoElement} controls src={src} height="600" width="1000" autoplay/>
    </div>
</div>
