from rest_framework import serializers


def StockSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Stock
        # fields = ('url', 'username', 'email', 'groups')