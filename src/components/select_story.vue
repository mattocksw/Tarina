<template>
    <div v-if="story_selected === false" class="ui content">
        <div class="top attached segment">
            <div class="ui large selection list">
                <div v-for="title in sortedTitles" v-on:click="click_select_story_item(title)" class="item">
                    <div class="content" style="color:teal; font-size: 1.5rem;" @contextmenu.prevent="$refs.rename_menu.open($event, {story: title})">{{title}}</div>
                </div>
            </div>
        </div>

        <vue-context ref="rename_menu">
            <div class="ui list" slot-scope="child">
                <div class="ui button" @click="click_rename_story($event.target.innerText, child.data)">Rename</div>
            </div>
        </vue-context>

        <vdialog modal_name="rename_story_dialog" :errors="errors" v-model="item_name" placeholder="" @opened="open_dialog" @closed="close_dialog"> </vdialog>

    </div>
</template>

<script>
    import { VueContext } from 'vue-context';
    import vdialog from '@/components/vdialog.vue'

    import Vue from 'vue'
    import { mapState } from 'vuex';
    export default
        {
            name: 'select_story',
            data: function () {
                return {
                    titles: [],
                    item_name: null,
                    errors: [],
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
            components:
            {
                vdialog,
                VueContext,
            },
            computed: mapState({
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
                
                story_selected: 'story_selected',
            }),
            methods:
            {
                click_select_story_item: function (title) {
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
                },
                open_dialog: function () {
                    this.vdialog_open = true
                },
                close_dialog: function () {
                    this.vdialog_open = false
                },
                click_rename_story: function (text, data) {
                    this.errors = []
                    var index = this.titles.indexOf(data.story)
                    this.$modal.show('rename_story_dialog',
                        {
                            title: 'Rename story:' + data.story,
                            text: 'Enter new name',
                            buttons:
                                [
                                    {
                                        title: 'Cancel',
                                        handler: () => {
                                            this.$modal.hide('rename_story_dialog')
                                        }
                                    },
                                    {
                                        title: 'Rename',
                                        default: true,
                                        handler: () => {
                                            this.axios.post('/rename_story',
                                                {
                                                    story_name: data.story,
                                                    new_name: this.item_name
                                                })
                                                .then(response => {
                                                    console.log(response)
                                                    this.errors = []

                                                    //update title in titles list
                                                    var temp = this.titles
                                                    temp[index] = this.item_name
                                                    Vue.delete(this.titles)
                                                    Vue.set(this.titles, temp)

                                                    this.item_name = null
                                                    this.$modal.hide('rename_story_dialog')

                                                })
                                                .catch(error => {
                                                    if (error.response.status === 404)
                                                        this.errors = ["could not connect to server"]
                                                    if (Array.isArray(error.response.data))
                                                        this.errors = error.response.data
                                                })
                                        }
                                    }
                                ]
                        });
                },
            },
            mounted()
            {
                //receive title from when new story is created
                this.$root.$on('new_story_created', data => { this.titles.push(data) })
                this.$root.$on('delete_story_completed', data => { Vue.delete(this.titles, this.titles.indexOf(data))})
            }
        }
</script>
