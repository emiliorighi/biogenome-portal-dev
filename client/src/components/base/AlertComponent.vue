<template>
    <b-alert 
        dismissible
        fade
        :show="showAlert"
        @dismissed="showAlert=false"
        :variant="alert.variant"
        v-if="alert.message"
        >
        {{alert.message}}
    </b-alert>
</template>
<script>
import {BAlert} from 'bootstrap-vue'
import {mapFields} from '../../utils/helper'
export default {
    computed:{
        ...mapFields({
            fields: ['showAlert'],
            module: 'submission',
            mutation: 'submission/setField'

        }),
        alert(){
            return this.$store.getters['submission/getAlert']
        }
    },
    components: {
        BAlert
    }
}
</script>