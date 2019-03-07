<template>
    <modal :name="modal_name"
           height="auto"
           :classes="['ui segment', this.params.class]"
           :width="width"
           :pivot-y="0.3"
           :adaptive="true"
           :clickToClose="clickToClose"
           :transition="transition"
           @before-open="beforeOpened"
           @before-close="beforeClosed"
           @opened="$emit('opened', $event)"
           @closed="$emit('closed', $event)">
        <div class="ui container">
            <div class="ui header"
                 v-if="params.title"
                 v-html="params.title || ''"></div>
            <div class="ui content form">
                <p v-if="errors.length">
                    <b> Please correct the following error(s):</b>
                    <ul>
                        <li v-for="error in errors">{{ error }}</li>
                    </ul>
                </p>
                <div class="field">
                    <label v-html="params.text || ''"></label>
                    <input v-if="input_field" type="text" name="value" v-model="value" :placeholder="placeholder">
                </div>
            </div>
        </div>
        <div class="actions"
             v-if="buttons">
            <button v-for="(button, i) in buttons"
                    :class="button.class || 'ui button'"
                    type="button"
                    :style="buttonStyle"
                    :key="i"
                    v-html="button.title"
                    @click.stop="click(i, $event)">
                {{button.title}}
            </button>
        </div>
        <div v-else class="vue-dialog-buttons-none"></div>
    </modal>
</template>
<script>
    export default {
        name: 'vdialog',
        props: {
            width: {
                type: [Number, String],
                default: 400
            },
            clickToClose: {
                type: Boolean,
                default: true
            },
            transition: {
                type: String,
                default: 'fade'
            },           
            errors: Array,
            value: String,
            //modal name must be unique
            modal_name: { 
                type: String,
                required: true
            },
            placeholder: {
                type: String,
                default: ''
            },
            input_field: {
                type: Boolean,
                default: true
            },
        },
        data() {
            return {
                params: {},
                defaultButtons: [{ title: 'CLOSE' }],
            }
        },
        watch:
        {
            value(val) {
                this.$emit('input', val)
            }
        },
        computed: {
            buttons() {
                return this.params.buttons || this.defaultButtons
            },
            /**
              * Returns FLEX style with correct width for arbitrary number of
              * buttons.
              */
            buttonStyle() {
                return {
                    flex: `1 1 ${100 / this.buttons.length}%`
                }
            }
        },
        methods: {
            beforeOpened(event) {
                window.addEventListener('keyup', this.onKeyUp)
                this.params = event.params || {}
                this.$emit('before-opened', event)
            },
            beforeClosed(event) {
                window.removeEventListener('keyup', this.onKeyUp)
                this.params = {}
                this.$emit('before-closed', event)
            },
            click(i, event, source = 'click') {
                const button = this.buttons[i]
                if (button && typeof button.handler === 'function') {
                    button.handler(i, event, { source })
                } else {
                    this.$modal.hide('dialog')
                }
            },
            onKeyUp(event) {
                if (event.which === 13 && this.buttons.length > 0) {
                    const buttonIndex =
                        this.buttons.length === 1
                            ? 0
                            : this.buttons.findIndex(button => button.default)
                    if (buttonIndex !== -1) {
                        this.click(buttonIndex, event, 'keypress')
                    }
                }
            }
        }
    }
</script>