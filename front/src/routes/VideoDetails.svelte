<script>
    import { beforeUpdate } from 'svelte';
    export let videoData;

    beforeUpdate(async () => {
        const res = await fetch(`http://localhost:8000/video/${videoData.uuid}/details`)
        const data = res.data();
        console.log(data);
    })
</script>

<div>
<h1>Video détails</h1>
<div>
</div>
</div>
