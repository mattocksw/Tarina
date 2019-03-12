
<template>
    <div v-if="editors.length" class="ui container">
        <div class="ui hidden divider"></div>
        <div v-for="editor in editors">
            <div class="ui top attached large block header" style="border-bottom: none;">
                <div class="ui two column stackable center aligned grid">
                    <div class="left aligned column">
                        {{editor.category}}/{{editor.item}}
                    </div>
                    <div class="right aligned column">
                        <a class="ui right aligned item">
                            <i v-on:click="close_editor(editor)" class="ui large close icon"></i>
                        </a>
                    </div>
                </div>
            </div>
            <div class="ui bottom attached segment" style="text-align: left;">
                <ck_editor v-bind:save_target="editor"> </ck_editor>
            </div>
            <div class="ui hidden divider"></div>
        </div>
    </div>
</template>

<script>
    import { mapState } from 'vuex';
    import ck_editor from '@/components/ck_editor.vue'
    export default
        {
            name: 'editors',
            components:
            {
                ck_editor,
            },
            computed: mapState({
                editors: 'editors',            
            }),
            methods: {
                close_editor: function (editor) {
                    this.$store.commit('delete_editor', { category: editor.category, item: editor.item })
                }
            },
            data: function () {
                return {
                    heigth: 100,
                }
            }
    }
</script>
