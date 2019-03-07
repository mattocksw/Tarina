<template>
    <div>
        <a v-on:click="click_new_story" class="item">New story</a>

        <vdialog modal_name="dialog" :errors="errors" v-model="story_name" placeholder="Title"> </vdialog>
    </div>
</template>

<script>
    import vdialog from '@/components/vdialog.vue'
    export default
        {
            name: 'new_story',
            components:
            {
                vdialog,
            },
            data: function () {
                return {
                    errors: [],
                    story_name: "",
                }
            },
            methods:
            {
                click_new_story: function (event) {
                    this.errors = []
                    this.$modal.show('dialog',
                        {
                            title: 'Create a new story',
                            text: 'Enter story title',
                            buttons:
                                [
                                    {
                                        title: 'Cancel',
                                        handler: () => {
                                            this.$modal.hide('dialog')
                                        }
                                    },
                                    {
                                        title: 'Create',
                                        default: true,
                                        handler: () => {
                                            this.axios.post('/new_story',
                                                {
                                                    story_name: this.story_name
                                                })
                                                .then(response => {
                                                    this.$store.commit('update_story_title', this.story_name)
                                                    this.errors = []                                                    
                                                    this.$store.commit('update_story_selected', true)
                                                    this.$store.commit('update_content', response.data)
                                                    //add title to list in sibling component
                                                    this.$root.$emit('new_story_created', this.story_name)
                                                    this.story_name = ""
                                                    this.$modal.hide('dialog')

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
