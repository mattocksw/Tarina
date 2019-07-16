<template>
    
    <div class="ui large horizontal menu">
        <new_story />
        <a class="ui item" href="/">Select story</a>
        <a class="ui item" v-on:click="new_tab">New tab</a>
        <a v-if="story_selected" class="ui item" v-bind:href="'/story/' + story_title + '/Chapters/story'">Download</a>
        <delete_story class="right menu" />
    </div>    
</template>

<script>   
    import new_story from '@/components/new_story.vue'
    import delete_story from '@/components/delete_story.vue'
    import { mapState } from 'vuex';
    export default
        {
            name: 'mainmenu',
            data: function () {
                return {
                    errors: [],
                }
            },
            computed: mapState({
                story_selected: 'story_selected',
                story_title: 'story_title',
            }),
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
