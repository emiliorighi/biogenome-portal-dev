<template>
<b-row>
    <b-col>
        <sample-details-component v-if="sample" :sample="sample"/>
    </b-col>
</b-row>

</template>
<script>
import SampleDetailsComponent from '../components/sample/SampleDetailsComponent.vue'
import portalService from '../services/DataPortalService'

export default {
    props: ['accession'],
    watch:{
        accession: function(accession){
            this.getSample(accession)
        }
    },
    data(){
        return {
            sample:null
        }
    },
    created(){
        this.getSample(this.accession)
    },
    methods:{
        getSample(accession){
        this.$store.dispatch('portal/showLoading')
        portalService.getSample(accession)
        .then(response => {
            this.sample = response.data
            this.$store.commit('portal/setBreadCrumb', {value: {text: accession, to: {name: 'sample-details', params:{accession: accession}}}})
            this.$store.dispatch('portal/hideLoading')
        })
        }
    },
    components: {
        SampleDetailsComponent
    }
}
</script>

