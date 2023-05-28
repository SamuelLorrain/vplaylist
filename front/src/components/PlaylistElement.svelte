<script>
    export let title;
    export let variant;
    $: formattedTitle = (title.length > 80 ? title.trim().substring(0, 80) + '...' : title);
</script>

<!-- TODO Should be a button or a link instead of a div on:click -->
<div on:click
     class={variant === 'active' ? 'playlist-element playlist-element-selected': 'playlist-element'}>
    <div class="playlist-element-icon">
    </div>
    <div class="playlist-element-title">
        {formattedTitle}
    </div>
</div>
