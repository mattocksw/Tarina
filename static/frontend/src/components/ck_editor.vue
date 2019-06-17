<style scoped>
    .hurray /deep/ .ck-editor__editable {
        max-height: var(--h);
    }
</style>

<style>
    a {
        color: black;
    }
</style>

<template>

    <div @click="handle_links" class="hurray" :style="cssProps">
        <ckeditor :editor="editor" v-model="editorData" :config="editorConfig" @ready="onEditorReady"></ckeditor>
        <div class="ui bottom attached segment" style="border: none; padding-bottom: 0;">
            <div @mousedown="start_resize" class="ui two column stackable center aligned grid">
                <div class="left aligned column">
                    {{status_bar_left}}
                </div>
                <div class="right aligned column">
                    <i class="ui expand arrows alternate vertical large icon"></i>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import Vue from 'vue'
    import store from '../store'

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

    function saveImage(data) {
        var story = store.state.story_title        
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
            watch: {
                save_target: function (newVal, oldVal) {
                    this.editor_object.config._config.save_target = newVal;
                    //get item content from server, don't know why this is needed, just a quick fix
                    this.axios.post('/get_item', {
                        story_name: this.editorConfig.story_name,
                        category: this.save_target.category,
                        item_name: this.save_target.item,
                    })
                        .then(response => {
                            this.editorData = response.data
                        })
                        .catch(error => {
                            console.log(error.response.data)
                        })
                }
            },
            data: function () {
                return {
                    editor_object: null,
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
                            ],
                            styles: [
                                'full',
                                'alignLeft',
                                'alignCenter',
                                'alignRight'
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
                },
            },
            created: function () {
                //get item content from server
                this.axios.post('/get_item', {
                        story_name: this.editorConfig.story_name,
                        category: this.save_target.category,
                        item_name: this.save_target.item,
                    })
                    .then(response => {
                        this.editorData = response.data
                        if (this.editorData.length === 0) {
                            this.editorData = "</p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p>"
                        }
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
                    this.$emit('start_resizing') //let parent know to start horizontal resize
                },
                stop_resize: function () {
                    this.resizing = false
                    this.$emit('stop_resizing')
                },
                resize_event: function (event) {
                    if (this.resizing) {
                        this.editor_height += event.movementY
                    }
                },
                onEditorReady: function (editor) {
                    this.displayStatus(editor)
                    //this.listenKeyup(editor)
                    //this.open_link(editor)
                    this.editor_object = editor
                    
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
                //used for autolinking
                listenKeyup: function (editor) {
                    editor.editing.view.document.on('keyup', (evt, data) => {
                        //if there is an existing link, remove it (not affected by arrow keys)
                        if ([37, 38, 39, 40].includes(data.keyCode) === false)
                        {
                            editor.execute('unlink')
                        }

                        //if key is enter or space check if item exists
                        if ([13, 32].includes(data.keyCode)) {
                            editor.model.change(writer => {

                                //get the position at the cursor
                                var insertPosition = editor.model.document.selection.getFirstPosition();                                
                                
                                //get cursor position as offset from topleft [element from top (0...n), letter offset (1...n)]
                                let pos = insertPosition.path
                                //if keyup was enter, move to above element
                                if(data.keyCode === 13)
                                    pos[0] = pos[0] - 1

                                //get current paragraph element as text
                                let p = data.domTarget.children[pos[0]].innerText                                
                                
                                //if just new line -> exit
                                if(p.length === 1)
                                    return

                                //if enter, move to end of line
                                if (data.keyCode === 13)
                                    pos[1] = p.length
                                //if space, substract it from offset (enter has end of line as final character so no need)
                                if (data.keyCode === 32)
                                    pos[1] = pos[1] - 1

                                //move to start of the word                               
                                let i = pos[1] - 1 //from offset to index
                                while (i >= 0) {
                                    if (p[i] === ' ') {
                                        break
                                    }
                                    i--
                                }                     

                                //get word (from index back to offset)
                                let word = p.substr(i + 1, pos[1])
                                console.log(word)

                                var start = [pos[0], pos[1] - word.length]
                                var end = pos                              

                                //check if word exists in content
                                var matches = []
                                var match_categories = []
                                var current_longest_word = 0
                                for (var c in store.state.content) {
                                    let items = store.state.content[c]
                                    for (var it = 0; it < items.length; it++) {
                                        if (items[it].length <= word.length && items[it].length >= current_longest_word && word.startsWith(items[it])) {
                                            //keep items that are closest to the typed word in length and shorter than typed word
                                            if (items[it].length > current_longest_word) {
                                                //collect items that are same length
                                                matches = []
                                                match_categories = []
                                                matches.push(items[it])
                                                match_categories.push(c)
                                                current_longest_word = items[it].length
                                            }
                                            else {
                                                matches.push(items[it])
                                                match_categories.push(c)
                                            }                                                                                       
                                        }                                            
                                    }                                    
                                }
                              
                                if (matches.length) {
                                    //keep one of the matches and hope it's the right one
                                    let linked_item = matches[0]
                                    let linked_category = match_categories[0]
                                   
                                    var range = editor.model.schema.getNearestSelectionRange(insertPosition)
                                    range.start.path = start
                                    range.end.path = end
                                    writer.setSelection(range);
                                    editor.execute('link', linked_category + "/" + linked_item)

                                    //clear selection
                                    //if keyup was enter, move to below element
                                    if (data.keyCode === 13) {
                                        range.start.path = [end[0] + 1, 0]
                                        range.end.path = range.start.path
                                    }
                                    else {
                                        range.start.path = [end[0], end[1] + 1]
                                        range.end.path = range.start.path
                                    }
                                    writer.setSelection(range);
                                }
                                
                            })
                        }                        
                    })
                },
                open_link: function (editor) {
                    
                    const linkActions = editor.plugins._plugins.get('LinkUI')
                    linkActions.on('change', (event) => {
                        console.log("handle link opening")
                    });
                },

                //https://dennisreimann.de/articles/delegating-html-links-to-vue-router.html
                handle_links: function (event) {                    
                    if (event.target.localName == 'a' && event.target.href) {
                        const { altKey, ctrlKey, metaKey, shiftKey, button, defaultPrevented } = event
                        
                        // don't handle with control keys
                        if (metaKey || altKey || ctrlKey || shiftKey) return
                        // don't handle when preventDefault called
                        if (defaultPrevented) return
                        
                        console.log("link:" + event.target.href)                                               
                    }
                    else {
                        console.log("clicked item not a link")
                    } 
                },
            },
            
        }
</script>
