<template>
    <div id="app" class="ui container" style="background-color:Gainsboro;">

        <item_selection />
        <!--Menu and main Required by sidebar -->

        <div class="ui center aligned basic segment">
            <h1 id="title" class="ui huge teal header"> {{story_title}} </h1>
        </div>

        <mainmenu />
        <!--
        <Menu />
        <main id="page-wrap">
    -->
        <select_story />

        <editors />
        <!--
        </main>
        -->
    </div>

    </template>

    <script>
        import mainmenu from '@/components/mainmenu.vue'
        import select_story from '@/components/select_story.vue'
        import item_selection from '@/components/item_selection.vue'
        import editors from '@/components/editors.vue'
        import { mapState } from 'vuex';

        export default
            {
                name: 'app',
                components:
                {
                    mainmenu,
                    select_story,
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
