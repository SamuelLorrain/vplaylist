<script>
    import PlaylistElement from './PlaylistElement.svelte';
    export let collection;
    export let clickOnVideoCallback;
    export let currentVideo;
</script>

<div class="playlist">
  <ul>
    {#each collection as video, i (video.uuid)}
      <li>
        {#if video.uuid === currentVideo.uuid}
          <PlaylistElement title={video.path} variant="active"/>
        {:else}
          <PlaylistElement title={video.path} on:click={() => clickOnVideoCallback(i)}/>
        {/if}
      </li>
    {/each}
  </ul>
</div>
