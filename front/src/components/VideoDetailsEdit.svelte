<script>
    export let data;
</script>

<div>
    <ul>
        <li>name: {data.name ?? ''}</li>
        <li>date_down: {data.date_down && new Date(data.date_down)}</li>
    </ul>
</div>
