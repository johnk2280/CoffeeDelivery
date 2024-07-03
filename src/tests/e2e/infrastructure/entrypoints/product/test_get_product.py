from httpx import AsyncClient

from tests.conftest import PrepDataYieldType


async def test_get_product_returns_200(
    async_client: AsyncClient,
    prep_data: PrepDataYieldType,
):

    response = await async_client.get('products')

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0] == prep_data['product']
