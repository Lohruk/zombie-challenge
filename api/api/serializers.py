from api.models import Report, Survivor, SurvivorTrade, SurvivorNames
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers


class ReadSurvivorSerializer(ModelSerializer):
    inventory = serializers.SerializerMethodField()

    class Meta:
        model = Survivor
        fields = (
            'id', 'name', 'age', 'gender', 'last_location_lat', 'last_location_long', 'inventory', 'infection',
            'infection_count',
        )

    def get_inventory(self, instance):
        return {f'Fiji Waters: {instance.fiji_water}', f'Campbell Soups: {instance.campbell_soup}',
                f'First Aid Pouchs: {instance.first_aid_pouch}', f'AK 47s: {instance.ak_47}'}


class WriteSurvivorSerializer(ModelSerializer):
    class Meta:
        model = Survivor
        fields = (
            'name', 'age', 'gender', 'last_location_lat', 'last_location_long', 'fiji_water',
            'campbell_soup', 'first_aid_pouch', 'ak_47'
        )


class UpdateCoordinateSerializer(ModelSerializer):
    class Meta:
        model = Survivor
        fields = ('id', 'last_location_lat', 'last_location_long')

    def update(self, instance, validated_data):
        sv_id = instance.id
        survivor = Survivor.objects.filter(id=sv_id).get()
        survivor.last_location_lat = validated_data['last_location_lat']
        survivor.last_location_long = validated_data['last_location_long']
        return Survivor.objects.filter(id=sv_id).update(last_location_lat=survivor.last_location_lat,
                                                        last_location_long=survivor.last_location_long)


class UpdateInfectionSerializer(ModelSerializer):
    class Meta:
        model = Survivor
        fields = ('id', 'infection', 'name')

    def update(self, instance, validated_data):
        # import ipdb
        # ipdb.set_trace()
        sv_id = instance.id
        survivor = Survivor.objects.filter(id=sv_id).get()
        infected = False
        count = int(survivor.infection_count + 1)
        if count > 5:
            raise ValueError('Survivor is already infected')
        if count == 5:
            infected = True
            print('Survivor has been infected.')
        return Survivor.objects.filter(id=sv_id).update(infection_count=count, infection=infected,
                                                        )


class TradeItemsSerializer(ModelSerializer):
    class Meta:
        model = SurvivorTrade
        fields = (
            'survivor_1_id', 'survivor_2_id', 'survivor_1_water', 'survivor_1_soup',
            'survivor_1_first_aid', 'survivor_1_gun', 'survivor_2_water', 'survivor_2_soup',
            'survivor_2_first_aid', 'survivor_2_gun'
        )

    def validate(self, data):
        survivor1 = Survivor.objects.filter(pk=data['survivor_1_id']).get()
        survivor2 = Survivor.objects.filter(pk=data['survivor_2_id']).get()
        if survivor1.infection:
            raise serializers.ValidationError("Survivor 1 is infected and can't engage in trades.")
        if survivor2.infection:
            raise serializers.ValidationError("Survivor 2 is infected and can't engage in trades.")
        trade_1 = int(data['survivor_1_water'] * 14 +
                      data['survivor_1_soup'] * 12 +
                      data['survivor_1_first_aid'] * 10 +
                      data['survivor_1_gun'] * 8
                      )

        trade_2 = int(data['survivor_2_water'] * 14 +
                      data['survivor_2_soup'] * 12 +
                      data['survivor_2_first_aid'] * 10 +
                      data['survivor_2_gun'] * 8
                      )
        if trade_1 == trade_2:
            return data
        else:
            raise serializers.ValidationError("The trade points aren't equal on both sides")

    def update(self, instance, validated_data):
        survivor1 = Survivor.objects.filter(id=validated_data['survivor_1_id']).get()
        survivor2 = Survivor.objects.filter(id=validated_data['survivor_2_id']).get()
        sv1_water = int(
            survivor1.fiji_water - validated_data['survivor_1_water'] + validated_data['survivor_2_water'])
        sv1_soup = int(
            survivor1.campbell_soup - validated_data['survivor_1_soup'] + validated_data['survivor_2_soup'])
        sv1_medkit = int(survivor1.first_aid_pouch - validated_data['survivor_1_first_aid'] + validated_data[
            'survivor_2_first_aid'])
        sv1_gun = int(
            survivor1.ak_47 - validated_data['survivor_1_gun'] + validated_data['survivor_2_gun'])
        sv2_water = int(
            survivor1.fiji_water + validated_data['survivor_1_water'] - validated_data['survivor_2_water'])
        sv2_soup = int(
            survivor1.campbell_soup + validated_data['survivor_1_soup'] - validated_data['survivor_2_soup'])
        sv2_medkit = int(survivor1.first_aid_pouch + validated_data['survivor_1_first_aid'] - validated_data[
            'survivor_2_first_aid'])
        sv2_gun = int(
            survivor1.ak_47 + validated_data['survivor_1_gun'] - validated_data['survivor_2_gun'])
        return [Survivor.objects.filter(id=survivor1.id).update(fiji_water=sv1_water, campbell_soup=sv1_soup,
                                                                first_aid_pouch=sv1_medkit, ak_47=sv1_gun),
                Survivor.objects.filter(id=survivor2.id).update(fiji_water=sv2_water, campbell_soup=sv2_soup,
                                                                first_aid_pouch=sv2_medkit, ak_47=sv2_gun)]


class ReadReportSerializer(ModelSerializer):
    full_report = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = ('report_date', 'full_report',)

    def get_full_report(self, instance):
        full_report = Report.objects.filter(pk=instance.id).get()
        return {f'Infected Survivor%: {full_report.infected_percent}%',
                f'Non-infected Survivor%: {full_report.non_infected_percent}%',
                f'Average Fiji Water per Survivor: {full_report.avg_water} un',
                f'Average Campbell Soup per Survivor: {full_report.avg_food} un',
                f'Average First Aid per Survivor: {full_report.avg_first_aid} un',
                f'Average AK47 per Survivor: {full_report.avg_gun} un',
                f'Total points lost due to infection: {full_report.lost_points}'
                }


class WriteReportSerializer(ModelSerializer):
    class Meta:
        model = Report
        fields = ('id', 'report_date')

    def create(self, validated_data):
        clean_survivors = Survivor.objects.filter(infection=False)
        infected_survivors = Survivor.objects.filter(infection=True)
        all_survivors = Survivor.objects.all()
        water = 0
        soup = 0
        medkit = 0
        gun = 0
        lost_water = 0
        lost_soup = 0
        lost_medkit = 0
        lost_gun = 0
        for survivor in clean_survivors:
            water += survivor.fiji_water
            soup += survivor.campbell_soup
            medkit += survivor.first_aid_pouch
            gun += survivor.ak_47
        avg_water = water / len(clean_survivors)
        avg_soup = soup / len(clean_survivors)
        avg_medkit = medkit / len(clean_survivors)
        avg_gun = gun / len(clean_survivors)
        for survivor in infected_survivors:
            lost_water += survivor.fiji_water
            lost_soup += survivor.campbell_soup
            lost_medkit += survivor.first_aid_pouch
            lost_gun += survivor.ak_47
        lost_total = (lost_water * 14 + lost_soup * 12 + lost_medkit * 10 + lost_gun * 8)
        Report.objects.all().delete()
        return Report.objects.create(infected_percent=(len(infected_survivors) * 100 / len(all_survivors)),
                                     non_infected_percent=(len(clean_survivors) * 100 / len(all_survivors)),
                                     avg_water=avg_water,
                                     avg_food=avg_soup,
                                     avg_first_aid=avg_medkit,
                                     avg_gun=avg_gun,
                                     lost_points=lost_total
                                     )
