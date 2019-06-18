<template>
    <div v-if="story_selected">
        <a v-on:click="click_delete_story" class="item">Delete story</a>

        <vdialog modal_name="delete_story_dialog" :errors="errors" :input_field="false"> </vdialog>
    </div>
</template>
<script>
    import { mapState } from 'vuex';
    import vdialog from '@/components/vdialog.vue'
    export default
        {
            name: 'delete_story',
            components:
            {
                vdialog,
            },
            data: function () {
                return {
                    errors: [],
                }
            },
            computed: mapState({
                story_selected: 'story_selected'                
            }),
            methods:
            {
                click_delete_story: function (event) {
                    this.errors = []
                    this.$modal.show('delete_story_dialog',
                        {
                            title: 'Delete ' + this.$store.state.story_title,
                            text: 'Are you sure you want to delete ' + this.$store.state.story_title,
                            buttons:
                                [
                                    {
                                        title: 'Cancel',
                                        handler: () => {
                                            this.$modal.hide('delete_story_dialog')
                                        }
                                    },
                                    {
                                        title: 'Delete',
                                        handler: () => {
                                            this.axios.post('/delete',
                                                {
                                                    story_name: this.$store.state.story_title
                                                })
                                                .then(response => {                                                    
                                                    this.errors = []                                                    
                                                    this.$store.commit('update_content', [])
                                                    //remove title from list in sibling component
                                                    this.$root.$emit('delete_story_completed', this.$store.state.story_title)
                                                    this.$store.commit('update_story_title',"Name of the story")
                                                    this.$store.commit('update_story_selected', false)
                                                    this.$modal.hide('delete_story_dialog')

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
            }
        }
</script>
