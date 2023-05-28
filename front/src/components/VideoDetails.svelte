<script>
    import VideoDetailsDisplay from  './VideoDetailsDisplay.svelte';
    import VideoDetailsEdit from  './VideoDetailsDisplay.svelte';
    import DownArrow from '../components/icons/DownArrow.svelte';
    import { beforeUpdate } from 'svelte';
    export let videoData;
    export let title;
    let data;
    let formData;
    let editMode = false;

    const fillFormData = () => {
        formData = structuredClone(data);
        console.log(formData);
    }

    const putData = () => {
        return fetch(`http://localhost:8000/video/${videoData.uuid}/details`, {
            method: 'PUT',
            body: JSON.stringify(formData),
            headers: {
                'Content-Type': 'application/json; chatset=utf-8'
            }
        })
    }

    // TODO xhr request
    let saveEdit = async () => {
        const response = await putData()
        console.log(response);
        // refresh video details
        editMode = false;
    }

    let onEdit = () => {
        fillFormData();
        editMode = true;
    }

    let offEdit = () => {
        editMode = false;
    }

    $: {
        fetch(`http://localhost:8000/video/${videoData.uuid}/details`)
            .then(result => result.json())
            .then(json => data = json)
    }
</script>

<div class="video-details-container">
    <h1>{title}</h1>
    <DownArrow/>
</div>
