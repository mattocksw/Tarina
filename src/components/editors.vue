
<template>
    <div v-if="editors.length" class="ui pusher container" ref="xposRef">
        <div class="ui hidden divider"></div>
        <div v-for="(editor, index) in editors">
            <div ref="editor_references">
                <div @mousedown="start_move(index)" class="ui top attached large block header" style="border-bottom: none;">
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
                    <ck_editor v-on:start_resizing="start_resize(index)" v-on:stop_resizing="stop_resize(index)" v-bind:save_target="editor"> </ck_editor>
                </div>
                <div class="ui hidden divider"></div>
            </div>    
        </div>
        <div class="ui vertical footer segment" style="padding-top: 100vh;">
            <div class="ui horizontal small divided link list">
                <a v-on:click="toggle_credits" class="item">Credits</a>
            </div>
            <div v-if="show_credits" class="ui content">
                <p>This software uses the followin third party libraries:</p>
                <p>vue: https://vuejs.org/ license: https://opensource.org/licenses/MIT </p>
                <p>Ckeditor 5: https://ckeditor.com/ license: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html </p>
                <p>bottle: https://bottlepy.org/docs/dev/ license: https://opensource.org/licenses/MIT</p> </p>
                <p>axios: https://github.com/axios/axios license: https://opensource.org/licenses/MIT</p> </p>
                <p>semantic ui: https://semantic-ui.com/ license: https://opensource.org/licenses/MIT</p> </p>
                <p>vue-draggable-resizable: https://github.com/mauricius/vue-draggable-resizable license: https://opensource.org/licenses/MIT</p> </p>
                <p>vuedraggable: https://github.com/SortableJS/Vue.Draggable license: https://opensource.org/licenses/MIT</p> </p>
                <p>vue-burger-menu: https://www.npmjs.com/package/vue-burger-menu license: https://opensource.org/licenses/MIT</p> </p>
                <p>vue-js-Dialog: https://github.com/euvl/vue-js-modal/blob/master/src/Dialog.vue license: https://opensource.org/licenses/MIT</p> </p>
                

            </div>
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
                selected_editor_index: 'selected_editor_index'
            }),
            watch: {
                selected_editor_index: function (new_length, old_length) {
                    if (old_length === 0)
                        return
                    //if new editor was created, scroll to the bottom of div containing all editors and footer
                    if (new_length > old_length) {
                        const new_div = this.$refs.xposRef
                        const top = new_div.getBoundingClientRect().bottom + window.scrollY

                        window.scrollTo({ top: top, behavior: 'smooth' })
                    }
                    //otherwise scroll to div
                    else {
                        const new_div = this.$refs.editor_references[this.selected_editor_index]
                        const top = new_div.getBoundingClientRect().top + window.scrollY

                        window.scrollTo({ top: top, behavior: 'smooth' })
                    }
                }
            },
            mounted: function () {
                window.addEventListener('mouseup', this.stop_move)
                window.addEventListener('mousemove', this.move_event)
            },
            data: function () {
                return {
                    moving: false,
                    resizing: false,
                    p_top: 0,
                    p_right: 0,
                    moving_index: 0,
                    show_credits: false,
                }
            },            
            methods: {
                close_editor: function (editor) {
                    this.$store.commit('delete_editor', { category: editor.category, item: editor.item })
                },
                toggle_credits: function () {
                    this.show_credits = !this.show_credits;
                },
                start_move: function (index) {
                    this.moving = true
                    this.moving_index = index
                },
                stop_move: function () {
                    this.moving = false
                    this.moving_index = 0
                },
                start_resize: function (index) {
                    this.resizing = true
                    this.moving_index = index
                },
                stop_resize: function (index) {
                    this.resizing = false
                    this.moving_index = 0
                },
                move_event: function (event) {

                    //check that editors exist
                    if (this.moving_index > this.editors.length)
                        return                    

                    //check that there is something to do
                    if (this.resizing || this.moving) {

                        var left, top, width

                        //Initialize/get values for clicked editor  
                        const move_div = this.$refs.editor_references[this.moving_index]
                        if (move_div.style.length > 2) {
                            left = parseInt(move_div.style.left)
                            top = parseInt(move_div.style.top)
                            width = parseInt(move_div.style.width)
                        }
                        else {
                            left = 0 //+ window.scrollX
                            top = 0 //+ window.scrollY
                            width = move_div.getBoundingClientRect().width
                        }

                        //move
                        if (this.moving) {
                            move_div.style.position = "relative"
                            move_div.style.top = top + event.movementY + "px"
                            move_div.style.left = left + event.movementX + "px"
                            move_div.style.width = width + "px"
                        }
                        //resizing
                        else {
                            move_div.style.position = "relative"
                            move_div.style.top = top + "px"
                            move_div.style.left = left + "px"
                            move_div.style.width = width + event.movementX + "px"
                        }

                    }
                   
                },
            },
            
    }
</script>
