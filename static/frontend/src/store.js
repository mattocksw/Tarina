import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

function getEditorIndex(editors, category, item) {
    for (var i = 0; i < editors.length; i++) {
        if (editors[i].category === category && editors[i].item === item)
            return i
    }
    return -1
}

export default new Vuex.Store({
  state: {
      story_selected: false,
      story_title: "Name of the story",
      content: [],
      editors: [],
  },
  mutations: {
      add_category(state, category) {
          Vue.set(state.content, category, [])
      },
      delete_category(state, category) {
          Vue.delete(state.content, category)
      },
      add_item(state, { category, item }) {
          var updated_list = state.content[category]
          updated_list.push(item)
          //delete previous and reset to trigger vue update
          Vue.delete(state.content, category)
          Vue.set(state.content, category, updated_list)
      },
      delete_item(state, { category, item }) {
          var updated_list = state.content[category]
          Vue.delete(updated_list, updated_list.indexOf(item))
          //delete previous and reset to trigger vue update
          Vue.delete(state.content, category)
          Vue.set(state.content, category, updated_list)
      },
      update_items(state, { category, items }) {
          Vue.delete(state.content, category)
          Vue.set(state.content, category, items)
      },
      update_content(state, content) {
          state.content = Object.assign({}, content)
      },
      update_story_selected(state, b) {
          state.story_selected = b
      },
      update_story_title(state, title) {
          state.story_title = title
      },
      add_editor(state, { category, item }) {
          //check that editor does not exist
          var combined = []
          combined["category"] = category
          combined["item"] = item
          if (getEditorIndex(state.editors, category, item) === -1)
              state.editors.push(combined)
      },
      delete_editor(state, { category, item }) {
          var index = getEditorIndex(state.editors, category, item)
          if (index !== -1)
              Vue.delete(state.editors, index)
      },
      delete_all_editors(state) {
          state.editors = []
      },
  },
  actions: {

  }
})
