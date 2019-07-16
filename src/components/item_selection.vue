
<style>
    .bm-burger-button {
        position: fixed;
        width: 36px;
        height: 30px;
        cursor: pointer;
    }    
    .bm-item-list {
        color: #b8b7ad;
        margin-left: 0%;
        font-size: 20px;
    }
    .bm-menu {
        height: 100%; /* 100% Full-height */
        width: 0; /* 0 width - change this with JavaScript */
        position: fixed; /* Stay in place */
        z-index: 1000; /* Stay on top */
        top: 0;
        left: 0;
        background-color: rgb(63, 63, 65); /* Black*/
        overflow-x: visible; /* Disable horizontal scroll */
        padding-top: 60px; /* Place content 60px from the top */
        transition: 0.5s; /*0.5 second transition effect to slide in the sidenav*/
    }
    .hb:hover {
        background-color: black;
    }
</style>


<template>
    <div v-if="story_selected">
        <Push isOpen disableOutsideClick @openMenu="handleOpenMenu" @closeMenu="handleCloseMenu">
            <a v-if="sidebar_open"><span>Directory</span></a>
            <div class="item">
                <a v-if="sidebar_open" v-on:click="click_new_item('folder')" href="#" class="ui inverted black left button"><span>New folder</span></a>
            </div>
            <transition v-if="sidebar_open" :duration="{ enter: 500, leave: 0 }">


                <div>
                    <div v-bind:class="{ active: show_loader }" class="ui inverted dimmer">
                        <div class="ui large text loader">Loading</div>
                    </div>

                    <div class="ui large vertical menu" style="background-color: rgb(63, 63, 65); border:none; max-height:60vh; height:auto;overflow-y:scroll;">
                        <div v-for="category in categories">
                            <div class="ui simple dropdown item" v-on:click="click_category(category)"  >

                                <i class="ui dropdown icon"></i>
                                <div style="color:teal; font-size: 20px; overflow-wrap: break-word;" @contextmenu.prevent="$refs.menu.open($event, {category: 'Categories', file: category})">{{category}}</div>

                                <div v-if="category===current_menu">
                                    <div class="item">
                                        <a class="ui inverted black left button" v-on:click="click_new_item">New file</a>
                                    </div>
                                    <draggable v-model="items" class="ui inverted divided selection list" @end="reorder_complete" style="max-height:300px; height:auto;overflow-y:scroll; ">
                                        <div v-for="item in items" class="item">
                                            <div style="overflow-wrap: break-word;color:white" 
                                                 @contextmenu.prevent="$refs.menu.open($event, {category: category, file: item})" 
                                                 v-on:click="click_item(item)" 
                                                 v-bind:class="{blue: item === selected_item}" 
                                                 class="ui hb header">{{item}}</div>
                                        </div>
                                    </draggable>
                                </div>


                            </div>
                        </div>
                    </div>



                </div>

            </transition">
            <div v-if="sidebar_open">
                <i v-if="message.length" class="ui borderless item"> {{message}} </i>
                <a class="right item">
                    <i v-on:click="refresh_content" class="sync icon"></i>
                </a>
            </div>
        </Push>
        <vdialog modal_name="add_item_dialog" :errors="errors" v-model="item_name" placeholder="" @opened="open_dialog" @closed="close_dialog"> </vdialog>
        <vdialog modal_name="delete_item_dialog" :errors="errors" :input_field="false" @opened="open_dialog" @closed="close_dialog"> </vdialog>
        <vdialog modal_name="rename_item_dialog" :errors="errors" v-model="item_name" placeholder="" @opened="open_dialog" @closed="close_dialog"> </vdialog>

        <vue-context ref="menu">
            <div class="ui list" slot-scope="child">
                <div class="ui black basic button" @click="optionClicked($event.target.innerText, child.data)">Rename</div>
                <div class="ui inverted red button" @click="optionClicked($event.target.innerText, child.data)">Delete</div>
            </div>


        </vue-context>

    </div>
</template>

<script>
    import draggable from 'vuedraggable'
    import vdialog from '@/components/vdialog.vue'
    import { mapState } from 'vuex';
    import { Push } from 'vue-burger-menu'

    import { VueContext } from 'vue-context';
    
    export default {
        name: 'item_selection',
        computed: mapState({
            story_selected: 'story_selected',
            content: 'content',
            story_title: 'story_title',
            //sort in ascending order
            categories: function () {
                function compare(a, b) {
                    var au = a.toUpperCase()
                    var bu = b.toUpperCase()
                    if (au < bu)
                        return -1;
                    if (au > bu)
                        return 1;
                    return 0;
                }

                return Object.keys(this.content).sort(compare)                    
            },
        }),
        components:
        {
            vdialog,
            draggable,
            Push,
            VueContext,
        },
        data: function ()
        {
            return {
                current_menu: "Categories",
                show_items: false,
                items: [],
                selected_item: null,
                errors: [],
                item_name: "",
                drag_timeout: null,
                message: "",
                show_loader: false,
                modify_categories: false,
                toggle_text: "Modify",
                sidebar_open: true,
                vdialog_open: false,
            }
        },
        watch: {
            story_title() {
                //reset all fields if title changes
                this.current_menu = "Categories"
                this.show_items= false
                this.items = []
                this.selected_item = null
                this.errors = []
                this.item_name = ""
                this.drag_timeout = null
                this.message = ""
                this.show_loader = false
                this.modify_categories = false
                this.toggle_text = "Modify"
                this.$store.commit('delete_all_editors')
                this.sidebar_open = true
                this.vdialog_open = false
            },
        },
        methods:
        {
            optionClicked: function (text, data) {
                
                this.current_menu = data.category
                this.selected_item = data.file

                if (text === 'Rename')
                    this.click_rename_item()
                if (text === 'Delete')
                    this.click_delete_item()
            },
            open_dialog: function () {
                this.vdialog_open = true
            },
            close_dialog: function () {
                this.vdialog_open = false
            },
            handleOpenMenu: function () {
                this.sidebar_open=true
            },
            handleCloseMenu: function () {
                this.sidebar_open = false
            },
            click_category: function (category)
            {
                console.log(this.vdialog_open)

                if (this.vdialog_open)
                    return

                if (this.current_menu === category)
                    return

                //if modify is disabled, open
                if (this.modify_categories === false) {
                    this.items = this.content[category]
                    this.show_items = true
                    this.current_menu = category
                }
                else {
                    this.selected_item = category
                }
            },
            click_item: function (item) {
                this.selected_item = item

                //open editor
                if (this.selected_item && this.current_menu !== "Categories")
                    this.$store.commit('add_editor', { category: this.current_menu, item: this.selected_item })                

            },
            click_back: function ()
            {
                this.selected_item = null
                this.items = []
                this.show_items = false
                this.current_menu = "Categories"
            },
            click_new_item: function (item_type="file")
            {
                if (this.vdialog_open === true)
                    return

                if (item_type === "folder")
                    this.current_menu = "Categories"

                this.errors = []
                this.$modal.show('add_item_dialog',
                    {
                        title: 'Create a new item in ' + this.current_menu,
                        text: 'Enter title for item',
                        buttons:
                            [
                                {
                                    title: 'Cancel',
                                    handler: () => {
                                        this.$modal.hide('add_item_dialog')
                                    }
                                },
                                {
                                    title: 'Create',
                                    default: true,
                                    handler: () => {
                                        this.axios.post('/new_item',
                                            {
                                                story_name: this.$store.state.story_title,
                                                item_name: this.item_name,
                                                item_category: this.current_menu
                                            })
                                            .then(response => {
                                                this.errors = []
                                                //if item added to categories, add it in root, otherwise append to existing
                                                if (this.current_menu === "Categories") {
                                                    this.$store.commit('add_category', this.item_name)
                                                    this.current_menu = this.item_name
                                                }
                                                else {
                                                    this.$store.commit('add_item', { category: this.current_menu, item: this.item_name })
                                                    this.items = this.content[this.current_menu]
                                                    this.selected_item = this.item_name
                                                    //open editor
                                                    if (this.selected_item && this.current_menu !== "Categories")
                                                        this.$store.commit('add_editor', { category: this.current_menu, item: this.selected_item })
                                                }                                    
                                                this.item_name = null
                                                this.$modal.hide('add_item_dialog')

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
            click_delete_item: function () {
                this.errors = []
                this.$modal.show('delete_item_dialog',
                    {
                        title: 'Delete ' + this.selected_item,
                        text: 'Are you sure you want to delete ' + this.selected_item,
                        buttons:
                            [
                                {
                                    title: 'Cancel',
                                    handler: () => {
                                        this.$modal.hide('delete_item_dialog')
                                    }
                                },
                                {
                                    title: 'Delete',
                                    handler: () => {
                                        this.axios.post('/delete_item',
                                            {
                                                story_name: this.$store.state.story_title,
                                                item_name: this.selected_item,
                                                item_category: this.current_menu
                                            })
                                            .then(response => {
                                                this.errors = []
                                                //if item deleted from categories, delete it from root, otherwise remove from existing
                                                if (this.current_menu === "Categories") {
                                                    this.$store.commit('delete_category', this.selected_item)
                                                    this.click_back()
                                                }
                                                else {                                                    
                                                    this.$store.commit('delete_item', { category: this.current_menu, item: this.selected_item })
                                                    this.$store.commit('delete_editor', { category: this.current_menu, item: this.selected_item })
                                                    this.items = this.content[this.current_menu]
                                                    this.selected_item = null                                                    
                                                }
                                                this.$modal.hide('delete_item_dialog')

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
            click_delete_folder: function () {
                this.selected_item = this.current_menu
                this.current_menu = "Categories"
                this.click_delete_item()

            },
            click_rename_item: function (target) {
                this.errors = []

                this.$modal.show('rename_item_dialog',
                    {
                        title: 'Rename ' + this.selected_item,
                        text: 'Enter new name',
                        buttons:
                            [
                                {
                                    title: 'Cancel',
                                    handler: () => {
                                        this.$modal.hide('rename_item_dialog')
                                    }
                                },
                                {
                                    title: 'Rename',
                                    default: true,
                                    handler: () => {
                                        this.axios.post('/rename_item',
                                            {
                                                story_name: this.$store.state.story_title,
                                                item_name: this.selected_item,
                                                item_category: this.current_menu,
                                                new_name: this.item_name
                                            })
                                            .then(response => {
                                                console.log(response)
                                                this.errors = []
                                                //if folder
                                                if (response.data.target !== 'file') {
                                                    this.$store.commit('rename_category', { category: this.selected_item, new_name: this.item_name })
                                                    this.current_menu = this.item_name
                                                    this.items = this.content[this.current_menu]
                                                    this.show_items = true

                                                }
                                                else {
                                                    this.$store.commit('rename_item', { category: this.current_menu, item: this.selected_item, new_name: this.item_name })
                                                    this.items = this.content[this.current_menu]                                                   
                                                }
                                                this.item_name = null
                                                this.$modal.hide('rename_item_dialog')

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
            reorder_complete: function () {
                this.message = "Saving..."
                //wait for other changes for a five seconds before saving to server
                clearTimeout(this.drag_timeout)

                //https://stackoverflow.com/questions/36209784/variable-inside-settimeout-says-it-is-undefined-but-when-outside-it-is-defined
                this.drag_timeout = setTimeout(() => {
                    this.axios.post('/reorder_items',
                        {
                            story_name: this.$store.state.story_title,
                            item_names: this.items,
                            item_category: this.current_menu
                        })
                        .then(response => {
                            console.log("reorder saved")
                            this.$store.commit('update_items', { category: this.current_menu, items: this.items })
                            this.message = "Saved changes to file order"

                        })
                        .catch(error => {
                            console.log("could not connect to server")
                            this.message = "Save failed"
                        })
                }, 2000)
            },
            refresh_content: function ()
            {
                this.show_loader = true
                this.axios.post('get_items',
                    {
                        story_name: this.$store.state.story_title,
                    })
                    .then(response => {
                        this.$store.commit('update_content', response.data)
                        this.message = "Contents reloaded"                        

                        if (this.current_menu !== "Categories") {
                            this.items = this.content[this.current_menu]
                        }
                        this.show_loader = false
                    })
                    .catch(error => {
                        console.log(error.response.data)
                        this.show_loader = false
                        this.message = "Reloading contents failed"
                    })
            },
            toggle_modify_categories: function () {
                if (this.modify_categories) {
                    this.modify_categories = false
                    this.toggle_text = "Modify"
                    this.selected_item = ""
                }
                else {
                    this.modify_categories = true
                    this.toggle_text = "Finish"
                    if(this.categories.length > 0)
                        this.selected_item = this.categories[0]
                }
            }
        }

}
</script>
