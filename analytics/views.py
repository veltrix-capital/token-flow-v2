from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from utils.graph import verify_graph_lib
from .models import User, Business, Event
from .serializers import UserSerializer, BusinessSerializer, EventSerializer

class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['get'], url_path='reward')
    def rewards(self, request, pk=None):
        user = self.get_object()
        reward_events = user.rewardevent_set.all()

        return Response(EventSerializer(instance=reward_events, many=True).data)

    @action(detail=True, methods=['get'], url_path='redeem')
    def redeems(self, request, pk=None):
        user = self.get_object()
        redeem_events = user.redeemevent_set.all()

        return Response(EventSerializer(instance=redeem_events, many=True).data)

    @action(detail=True, methods=['get'], url_path='transfer-in')
    def trasnfer_ins(self, request, pk=None):
        user = self.get_object()
        redeem_events = user.redeemevent_set.all()

        return Response(EventSerializer(instance=redeem_events, many=True).data)

    @action(detail=True, methods=['get'], url_path='transfer-out')
    def transfer_outs(self, request, pk=None):
        user = self.get_object()
        transfers_sent = user.transfers_out.all()

        return Response(EventSerializer(instance=transfers_sent, many=True).data)

    @action(detail=True, methods=['get'], url_path='swap')
    def events(self, request, pk=None):
        user = self.get_object()
        swap_events = user.swaps_out.all().union(user.swaps_in.all())

        return Response(EventSerializer(instance=swap_events, many=True).data)

    @action(detail=True, methods=['get'], url_path='events')
    def events(self, request, pk=None):
        user = self.get_object()

        reward_events = user.rewardevent_set.all()
        redeem_events = user.redeemevent_set.all()
        transfers_sent = user.transfers_out.all()
        transfers_received = user.transfers_in.all()
        swap_events = user.swaps_out.all().union(user.swaps_in.all())

        return Response({
            'reward': EventSerializer(instance=reward_events, many=True).data,
            'redeem': EventSerializer(instance=redeem_events, many=True).data,
            'transfer-out': EventSerializer(instance=transfers_sent, many=True).data,
            'trasnfer-in': EventSerializer(instance=transfers_received, many=True).data,
            'swap': EventSerializer(instance=swap_events, many=True).data,
        })

class BusinessViewSet(ReadOnlyModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer

    @action(detail=True, methods=['get'], url_path='rewards')
    def rewards(self, request, pk=None):
        # TODO: Get reward event list
        return Response()

    @action(detail=True, methods=['get'], url_path='redeems')
    def redeems(self, request, pk=None):
        # TODO: Get redeem event list
        return Response()

    @action(detail=True, methods=['get'], url_path='balances')
    def balances(self, request, pk=None):
        # TODO: Get balance of token of all users (skip users without token)
        # Balance = total inflow - total outflow

        return Response()

    @action(detail=True, methods=['get'], url_path='token-inflows')
    def token_inflows(self, request, pk=None):
        """
            Get list of token inflows (with reward, transfer, and swaps) for a user

            Returns:
                The all detailed sources of received token
        """

        business = self.get_object()

        user_address = request.query_params.get('user')
        if not user_address:
            return Response({'error': 'user query parameter is required'}, status=400)

        try:
            User.objects.get(address=user_address)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)


        reward_events = business.rewardevent_set.all()
        redeem_events = business.redeemevent_set.all()
        transfer_events = business.transferevent_set.all()
        swaps_out = business.swaps_out.all()
        swaps_in = business.swaps_in.all()

        edges = []
        for event in reward_events:
            edges.append({ 'from': business.owner, 'to': event.user.address, 'weight': event.amount })

        for event in redeem_events:
            edges.append({ 'from': event.user.address, 'to': business.owner, 'weight': event.amount })

        for event in transfer_events:
            edges.append({ 'from': event.from_user.address, 'to': event.to_user.address, 'weight': event.amount })

        for event in swaps_in:
            edges.append({ 'from': event.to_user.address, 'to': event.from_user.address, 'weight': event.to_amount })

        for event in swaps_out:
            edges.append({ 'from': event.from_user.address, 'to': event.to_user.address, 'weight': event.from_amount })

        graph = get_graph(edges=[get_reversed_edge(e) for e in edges], weighted=True, multi=False)
        movements = []

        while True:
            token_flow = [user_address]
            
            visited_edges = {}
            def find_token_movement(address, min_weight):
                if address == business.owner:
                    return min_weight

                for from_address, edge in graph[address].items():
                    weight = edge['weight']

                    edge_id = address + '-' + from_address
                    if edge_id in visited_edges:
                        continue

                    visited_edges[edge_id] = True

                    if weight > 0:
                        token_flow.append(from_address)
                        return find_token_movement(from_address, min(min_weight, weight))

                return min_weight

            amount = find_token_movement(user_address, 1e10)
            if len(token_flow) == 1:
                break

            for i in range(len(token_flow) - 1):
                edge = graph[token_flow[i]][token_flow[i+1]]

                graph[token_flow[i]][token_flow[i+1]].update({ 'weight': edge['weight'] - amount })

            token_flow.reverse()
            movements.append({
                'path': token_flow,
                'amount': amount
            })

        return Response(movements)

    @action(detail=True, methods=['get'], url_path='token-outflows')
    def token_outflows(self, request, pk=None):
        """
            Get list of token spends (with redeem, transfer, swap) for a user

            Returns:
                The all detailed usage of received token
        """
        # TODO: Develop endpoint in the similar way to token_inflows

        return Response()

class EventViewSet(ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
