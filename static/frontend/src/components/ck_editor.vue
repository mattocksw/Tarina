<style scoped>
    .hurray /deep/ .ck-editor__editable {
        max-height: var(--h);
    }
</style>


<template>

    <div class="hurray" :style="cssProps">
        <ckeditor :editor="editor" v-model="editorData" :config="editorConfig" @ready="onEditorReady"></ckeditor>
        <div class="ui bottom attached segment" style="border: none; padding-bottom: 0;">
            <div class="ui two column stackable center aligned grid">
                <div class="left aligned column">
                    {{status_bar_left}}
                </div>
                <div class="right aligned column">
                    <i @mousedown="start_resize" class="ui expand arrows alternate icon"></i>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import Vue from 'vue'

    import ClassicEditor from '@ckeditor/ckeditor5-editor-classic/src/classiceditor';
    import EssentialsPlugin from '@ckeditor/ckeditor5-essentials/src/essentials';
    import AutoformatPlugin from '@ckeditor/ckeditor5-autoformat/src/autoformat';
    import BoldPlugin from '@ckeditor/ckeditor5-basic-styles/src/bold';
    import ItalicPlugin from '@ckeditor/ckeditor5-basic-styles/src/italic';
    import UnderlinePlugin from '@ckeditor/ckeditor5-basic-styles/src/underline';
    import StrikethroughPlugin from '@ckeditor/ckeditor5-basic-styles/src/strikethrough';
    import CodePlugin from '@ckeditor/ckeditor5-basic-styles/src/code';
    import SubscriptPlugin from '@ckeditor/ckeditor5-basic-styles/src/subscript';
    import SuperscriptPlugin from '@ckeditor/ckeditor5-basic-styles/src/superscript';
    import HeadingPlugin from '@ckeditor/ckeditor5-heading/src/heading';
    import ImagePlugin from '@ckeditor/ckeditor5-image/src/image';
    import ImageCaptionPlugin from '@ckeditor/ckeditor5-image/src/imagecaption';
    import ImageStylePlugin from '@ckeditor/ckeditor5-image/src/imagestyle';
    import ImageToolbarPlugin from '@ckeditor/ckeditor5-image/src/imagetoolbar';
    import ImageUploadPlugin from '@ckeditor/ckeditor5-image/src/imageupload';
    import LinkPlugin from '@ckeditor/ckeditor5-link/src/link';
    import ListPlugin from '@ckeditor/ckeditor5-list/src/list';
    import ParagraphPlugin from '@ckeditor/ckeditor5-paragraph/src/paragraph';
    import Autosave from "@ckeditor/ckeditor5-autosave/src/autosave"
    import PendingActions from '@ckeditor/ckeditor5-core/src/pendingactions';
    import Alignment from '@ckeditor/ckeditor5-alignment/src/alignment';
    import FontPlugin from '@ckeditor/ckeditor5-font/src/font';
    import HighlightPlugin from '@ckeditor/ckeditor5-highlight/src/highlight';
    import PasteFromOfficePlugin from '@ckeditor/ckeditor5-paste-from-office/src/pastefromoffice';
    import TablePlugin from '@ckeditor/ckeditor5-table/src/table';
    import TableToolbarPlugin from '@ckeditor/ckeditor5-table/src/tabletoolbar';
    import SimpleUploadImagePlugin from '@samhammer/ckeditor5-simple-image-upload-plugin/src/simple-upload-image-plugin'


    function saveData(data, story, target) {
        return Vue.prototype.axios.post('/save',
            {
                story_name: story,
                category: target.category,
                item_name: target.item,
                content: data,
            })
    }

    function reverse_escape_html(str) {
        var textArea = document.createElement('textarea');
        textArea.innerHTML = str;
        return textArea.value;
    }

    function saveImage(data) {
        var story = reverse_escape_html(document.getElementById('title').innerText);        
        let formData = new FormData();
        formData.append("image", data);
        formData.append("story_name", story);
        return Vue.prototype.axios.post('/save_image',
            formData,
            {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
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
                    editor_height: 500,
                    resizing: false,
                    status_bar_left: "",
                    status_bar_right: "",
                    editor: ClassicEditor,
                    editorData: "",
                    editorConfig:
                    {
                        plugins: [
                            EssentialsPlugin,
                            AutoformatPlugin,
                            BoldPlugin,
                            ItalicPlugin,
                            UnderlinePlugin,
                            StrikethroughPlugin,
                            CodePlugin,
                            SubscriptPlugin,
                            SuperscriptPlugin,
                            HeadingPlugin,
                            ImagePlugin,
                            ImageCaptionPlugin,
                            ImageStylePlugin,
                            ImageToolbarPlugin,
                            ImageUploadPlugin,
                            LinkPlugin,
                            ListPlugin,
                            ParagraphPlugin,
                            Autosave,
                            PendingActions,
                            Alignment,
                            FontPlugin,
                            HighlightPlugin,
                            PasteFromOfficePlugin,
                            TablePlugin,
                            TableToolbarPlugin,
                            SimpleUploadImagePlugin
                        ],

                        toolbar:
                        {
                            items: [
                                'heading',
                                '|',
                                'fontSize', 'fontFamily',                                
                                'alignment:left', 'alignment:right', 'alignment:center', 'alignment:justify',
                                'bold', 'italic', 'underline', 'strikethrough', 'code', 'subscript', 'superscript',
                                'highlight',
                                'link',
                                'bulletedList',
                                'numberedList',
                                'insertTable',
                                'imageUpload',
                                'undo',
                                'redo'
                            ]
                        },
                        table: {
                            contentToolbar: ['tableColumn', 'tableRow', 'mergeTableCells']
                        },
                        simpleImageUpload: {                            
                            //image upload
                            onUpload: file => {
                                return saveImage(file).then(response => {
                                    var address = response.data
                                    return Promise.resolve('/' + address.story_folder + '/' + address.file_name);
                                })
                            },
                        },
                        image: {
                            toolbar: [
                                'imageStyle:full',
                                'imageStyle:side',
                                'imageStyle:alignLeft',
                                'imageStyle:alignCenter',
                                'imageStyle:alignRight',
                                '|',
                                'imageTextAlternative'
                            ]
                        },
                        fontSize: {
                            options: [
                                9,
                                11,
                                13,
                                'default',
                                17,
                                19,
                                21
                            ]
                        },
                        highlight: {
                            options:
                            [                                
                                { model: 'yellowMarker', class: 'marker-yellow', title: 'Yellow Marker', color: 'var(--ck-highlight-marker-yellow)', type: 'marker' },
                                { model: 'greenMarker', class: 'marker-green', title: 'Green marker', color: 'var(--ck-highlight-marker-green)', type: 'marker' },
                                { model: 'pinkMarker', class: 'marker-pink', title: 'Pink marker', color: 'var(--ck-highlight-marker-pink)', type: 'marker' },
                                { model: 'blueMarker', class: 'marker-blue', title: 'Blue marker', color: 'var(--ck-highlight-marker-blue)', type: 'marker' },                                
                                { model: 'redPen', class: 'pen-red', title: 'Red pen', color: 'var(--ck-highlight-pen-red)', type: 'pen' },
                                { model: 'greenPen', class: 'pen-green', title: 'Green pen', color: 'var(--ck-highlight-pen-green)', type: 'pen' }                             
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
            computed: {
                cssProps() {
                    return {
                        '--h': this.editor_height + "px",
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
            mounted: function () {
                window.addEventListener('mouseup', this.stop_resize)
                window.addEventListener('mousemove', this.resize_event)
            },
            methods:
            {
                start_resize: function () {
                    this.resizing = true
                },
                stop_resize: function () {
                    this.resizing = false
                },
                resize_event: function (event) {
                    if (this.resizing) {
                        this.editor_height += event.movementY
                    }
                },
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
