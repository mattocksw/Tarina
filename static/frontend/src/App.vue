<template>
    <div id="app" class="ui container" style="background-color:Gainsboro;">

        <div class="ui center aligned basic segment">
            <div class="ui text">
                <h1 class="ui header"> {{story_title}} </h1>
            </div>
        </div>

        <mainmenu />

        <editors />

        <item_selection />



    </div>
</template>

<script>
    import mainmenu from '@/components/mainmenu.vue'
    import item_selection from '@/components/item_selection.vue'
    import editors from '@/components/editors.vue'
    import { mapState } from 'vuex';

    export default
        {
            name: 'app',
            components:
            {
                mainmenu,
                item_selection,
                editors,
            },
            data: function ()
            {
                return {
                    editors: [],
                    content: [],
                    chapters: [],
                }
            },
            computed: mapState({
                story_title: 'story_title'
            })
                    
        }  
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
