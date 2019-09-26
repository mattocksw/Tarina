<template>
    
    <div class="ui large horizontal menu">
        <new_story />
        <div class="ui simple dropdown item">
            Start page
            <div class="attached menu" style="border-radius: 0px; border: 0px;">
                <a class="ui item" v-on:click="new_tab">New tab</a>
                <a class="ui item" href="/">Current tab</a>
            </div>
        </div>           
        <div v-if="story_selected" class="ui simple dropdown item">
            Download story
            <div class="attached menu" style="border-radius: 0px; border: 0px;">
                <a class="item" v-bind:href="'/download/html/' + story_title" download>Html</a>
                <a class="item" v-bind:href="'/download/docx/' + story_title" download>Docx</a>
            </div>
        </div>
        
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
