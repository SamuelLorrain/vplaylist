<script>
    export let collection;
    export let clickOnVideoCallback;
    export let currentVideo;
</script>

<div class="playlist">
  {#each collection as video, i (video.uuid)}
      <div class="playlist-element">
          {#if video.uuid === currentVideo.uuid}
              <div><b>{video.path}</b></div>
          {:else}
              <button on:click={() => clickOnVideoCallback(i)}>{video.path}</button>
          {/if}
      </div>
  {/each}
</div>

<style>
.playlist {
    overflow-y: scroll;
    height: 50vh;
}

.playlist button {
    border: 0;
    background: inherit;
    cursor: pointer;
    text-align: start;
}
</style>
