<template>
    <div>
        <ckeditor :editor="editor" v-model="editorData" :config="editorConfig" @ready="onEditorReady"></ckeditor>
        <div class="ui bottom attached segment" style="border-top: none;">
            <div class="ui two column stackable center aligned grid">
                <div class="left aligned column">
                    {{status_bar_left}}
                </div>
                <div class="right aligned column">
                    {{status_bar_right}}
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import Vue from 'vue'

    import ClassicEditor from '@ckeditor/ckeditor5-editor-classic/src/classiceditor';

    import EssentialsPlugin from '@ckeditor/ckeditor5-essentials/src/essentials';
    import BoldPlugin from '@ckeditor/ckeditor5-basic-styles/src/bold';
    import ItalicPlugin from '@ckeditor/ckeditor5-basic-styles/src/italic';
    import LinkPlugin from '@ckeditor/ckeditor5-link/src/link';
    import ParagraphPlugin from '@ckeditor/ckeditor5-paragraph/src/paragraph';
    import Autosave from "@ckeditor/ckeditor5-autosave/src/autosave"
    import PendingActions from '@ckeditor/ckeditor5-core/src/pendingactions';


    function saveData(data, story, target) {
        return Vue.prototype.axios.post('/save',
            {
                story_name: story,
                category: target.category,
                item_name: target.item,
                content: data,
            })
    }

    export default
        {
            name: 'ck_editor',
            props: {
                save_target: {
                    type: Array,
                    required: true
                },
            },
            data: function () {
                return {
                    status_bar_left: "",
                    status_bar_right: "",
                    editor: ClassicEditor,
                    editorData: "",
                    editorConfig:
                    {
                        plugins: [
                            EssentialsPlugin,
                            BoldPlugin,
                            ItalicPlugin,
                            LinkPlugin,
                            ParagraphPlugin,
                            Autosave,
                            PendingActions
                        ],

                        toolbar:
                        {
                            items: [
                                'bold',
                                'italic',
                                'link',
                                'undo',
                                'redo'
                            ]
                        },
                        autosave: {
                            save(editor) {
                                return saveData(editor.getData(), editor.config._config.story_name, editor.config._config.save_target)
                            }
                        },
                        save_target: this.save_target,
                        story_name: this.$store.state.story_title,
                    }
                }
            },
            created: function () {
                //get item content from server
                this.axios.post('/get_item', {
                        story_name: this.editorConfig.story_name,
                        category: this.editorConfig.save_target.category,
                        item_name: this.editorConfig.save_target.item,
                    })
                    .then(response => {
                        this.editorData = response.data
                    })
                    .catch(error => {
                        console.log(error.response.data)
                    })
               
            },
            methods:
            {
                onEditorReady: function (editor) {
                    this.displayStatus(editor)
                },
                displayStatus: function (editor) {
                    //display save status
                    const pendingActions = editor.plugins._plugins.get('PendingActions')

                    pendingActions.on('change:hasAny', (evt, propertyName, newValue) => {
                        if (newValue) {
                            this.status_bar_left = "Saving..."
                        } else {
                            this.status_bar_left = "Saved"
                        }
                    });
                },
            },
            
        }
</script>
