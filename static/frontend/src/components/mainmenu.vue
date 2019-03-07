<template>
    <div class="ui horizontal menu">
        <select_story />
        <new_story />
        <delete_story class="right menu"/>
    </div>
</template>

<script>
    import select_story from '@/components/select_story.vue'
    import new_story from '@/components/new_story.vue'
    import delete_story from '@/components/delete_story.vue'
    export default
        {
            name: 'mainmenu',
            data: function () {
                return {
                    story_name: null,
                    errors: [],
                }
            },            
            components:
            {
                select_story,
                new_story,
                delete_story,
            },
                      
            methods:
            {
                
            },
        }
</script>
