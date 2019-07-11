<template>
    
    <div class="ui large horizontal menu">
        <new_story />
        <a class="ui item" href="/">Select story</a>
        <a class="ui item" v-on:click="new_tab">New tab</a>
        <delete_story class="right menu" />
    </div>    
</template>

<script>   
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
                new_story,
                delete_story,
            },
                      
            methods:
            {
                new_tab: function () {
                    window.open("/")
                }
            },
        }
</script>
