<template>
    <div class="ui simple dropdown item">
        Select story
        <i class="dropdown icon"></i>
        <div class="menu" style="overflow:auto; max-height: 50vh; max-width: 50vw;">
            <a v-for="title in sortedTitles" v-on:click="click_select_story_item" class="item">{{title}}</a>
            <a v-if="titles.length === 0" class="red item">Empty</a>
        </div>
    </div>
</template>

<script>
    function reverse_escape_html(str) {
        var textArea = document.createElement('textarea');
        textArea.innerHTML = str;
        return textArea.value;
    }

    import Vue from 'vue'
    export default
        {
            name: 'select_story',
            data: function () {
                return {
                    titles: [],
                }
            },       
            created: function () {
                this.axios.get('get_stories')
                    .then(response => {
                        this.titles = response.data
                    })
                    .catch(error => {
                        console.log(error.response.data)
                    })
            },
            computed:
            {
                sortedTitles: function () {
                    function compare(a, b) {
                        var au = a.toUpperCase()
                        var bu = b.toUpperCase()
                        if (au < bu)
                            return -1;
                        if (au > bu)
                            return 1;
                        return 0;
                    }

                    return this.titles.slice().sort(compare);
                },
            },
            methods:
            {
                click_select_story_item: function (event) {
                    var title = reverse_escape_html(event.srcElement.innerHTML)
                    this.axios.post('get_items',
                        {
                            story_name: title,
                        })
                        .then(response => {
                            this.$store.commit('update_story_title', title)
                            this.$store.commit('update_story_selected', true)
                            this.$store.commit('update_content', response.data)
                        })
                        .catch(error => {
                            console.log(error.response.data)
                        })
                }
            },
            mounted()
            {
                //receive title from when new story is created
                this.$root.$on('new_story_created', data => { this.titles.push(data) })
                this.$root.$on('delete_story_completed', data => { Vue.delete(this.titles, this.titles.indexOf(data))})
            }
        }
</script>
