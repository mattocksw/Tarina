<template>
    <div v-if="story_selected">
        <div class="ui visible very wide vertical sidebar menu">
            <h3 class="ui top attached block header"> {{story_title}} </h3>

            <h4 class="ui attached center aligned header">
                <a v-if="show_items" v-on:click="click_back" class="left aligned">
                    <i class="arrow left icon"></i>
                </a>
                {{current_menu}}
            </h4>
            <div class="ui attached segment">
                <div>


                    <a v-if="show_items" v-on:click="click_new_item" class="item">New file</a>
                    <a v-else v-on:click="click_new_item" class="item">New folder</a>

                </div>
            </div>

            <div class="ui attached segment">
                <div v-bind:class="{ active: show_loader }" class="ui inverted dimmer">
                    <div class="ui large text loader">Loading</div>
                </div>
                <div v-if="show_items">
                    <draggable v-model="items" class="ui divided selection list" @end="reorder_complete">
                        <div v-for="item in items" class="item">
                            <div class="content">
                                <div v-on:click="click_item(item)" v-bind:class="{blue: item === selected_item}" class="ui header">{{item}}</div>
                            </div>
                        </div>
                    </draggable>
                </div>
                <div v-else class="ui divided selection list">
                    <div v-for="category in categories" class="item">
                        <div class="content">
                            <div v-on:click="click_category(category)" v-bind:class="{blue: category === selected_item}" class="ui header">{{category}}</div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="ui attached menu" style="border-bottom: none;">
                <i v-if="message.length" class="ui borderless item"> {{message}} </i>
                <a class="right item">
                    <i v-on:click="refresh_content" class="sync icon"></i>
                </a>
            </div>

            <div v-if="show_items" class="ui attached segment">
                <a v-on:click="click_delete_item" v-if="selected_item" class="item">Delete file</a>
                <a v-else class="item" data-tooltip="No file selected">Delete file</a>

                <a v-if="selected_item" v-on:click="click_rename_item('file')" class="item">Rename file</a>
                <a v-else class="item" data-tooltip="No file selected">Rename file</a>

                <a v-on:click="click_rename_item('folder')" class="item">Rename folder</a>
            </div>

        </div>
        <vdialog modal_name="add_item_dialog" :errors="errors" v-model="item_name" placeholder=""> </vdialog>
        <vdialog modal_name="delete_item_dialog" :errors="errors" :input_field="false"> </vdialog>
        <vdialog modal_name="rename_item_dialog" :errors="errors" v-model="item_name" placeholder=""> </vdialog>

    </div>
</template>

<script>
    import draggable from 'vuedraggable'
    import vdialog from '@/components/vdialog.vue'
    import { mapState } from 'vuex';
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
            },
        },
        methods:
        {
            click_category: function (category)
            {
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
            click_new_item: function ()
            {
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
            click_rename_item: function (target) {
                this.errors = []
                var tmp = ''
                if (target === 'file')
                    tmp = this.selected_item
                else
                    tmp = this.current_menu

                this.$modal.show('rename_item_dialog',
                    {
                        title: 'Rename ' + tmp,
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
                                                new_name: this.item_name,
                                                target: target
                                            })
                                            .then(response => {
                                                this.errors = []
                                                //if folder
                                                if (response.data.target !== 'file') {
                                                    this.$store.commit('rename_category', { category: this.current_menu, new_name: this.item_name })
                                                    this.current_menu = this.item_name
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
