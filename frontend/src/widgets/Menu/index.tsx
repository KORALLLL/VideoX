import { Flex, useTheme } from '@chakra-ui/react'
import MenuButton from 'features/menu-button/ui/MenuButton'
import { useNavigate, useMatch } from 'react-router-dom'
import {
  Play,
  History,
} from 'shared/iconpack'
import { PageRoutes } from 'shared/config/pages/PageRoutes'
import { Box } from 'shared/ui'

function Menu() {
  const navigate = useNavigate()
  const theme = useTheme()
  const gray600 = theme.colors.gray['600']
  const isMain = useMatch(PageRoutes.Main)
  const isHistory = useMatch(PageRoutes.History)
  
  return (
    <Flex
      maxW={'42px'}
      w={'100%'}
      flexDir={'column'} 
      gap={'24px'} 
      pt={'176px'}
      alignItems={'center'}
      bgColor={'transparent'}
      position="fixed"
      left="40px"
      top="30px"
      bottom="30px"
    >
      <MenuButton
        onClick={() => navigate(PageRoutes.Main)}
        active={isMain ? true : false}
      >
        <Box w={{ sm: '20px', base: '20px', md: '25px', lg: '30px' }}>
          <Play
            width={'100%'}
            height={'auto'}
            color={gray600}
          />
        </Box>
      </MenuButton>
      <MenuButton
        onClick={() => navigate(PageRoutes.History)}
        active={isHistory ? true : false}
      >
        <Box w={{ sm: '20px', base: '20px', md: '25px', lg: '30px' }}>
          <History
            width={'100%'}
            height={'auto'}
            color={gray600}
          />
        </Box>
      </MenuButton>
    </Flex>
  )
}

export { Menu }
